from .models import Fund, FundOption
from rest_framework import viewsets
from .serializers import FundSerializer, FundOptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from loans.permissions import IsBankerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from users.models import User
from loans.helpers import toJSON
from bank.models import Bank
from bank.views import get_or_create_bank
from django.shortcuts import get_object_or_404
from rest_framework import status as HTTPStatus

from decimal import *
import math
import stripe

stripe.api_key = "sk_test_51JQJmIDP01ev1pnVi4luE9KefOuioXzgtLUrckNi5qJJmeiBNtXstuXah3BEsaG80eqWz0ZZA5oel4kjEHeveN9D00yUcx8ERF"
# Create your views here.


class FundOptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrReadOnly,)
    queryset = FundOption.objects.all()
    serializer_class = FundOptionSerializer


class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    def create(self, request):
        # Parse the body into valid JSON.
        body = toJSON(request.body)

        """
            - Make sure that a Funder can only add Funds from himself.
            - Make sure that the request is done by a Funder.
        """
        if request.user.id != body['funder'] or request.user.user_type != User.FUNDER:
            raise PermissionDenied()

        # Gather the data from the request body.
        funder = User.objects.get(pk=body['funder'])
        amount = Decimal(body['amount'])
        option = FundOption.objects.get(pk=body['option'])

        # Make sure the amount fits in the range of the option
        if amount > option.maximum_amount or amount < option.minimum_amount:
            return Response({"message": "Incorrect amount for your plan"})

        # Save the fund with the data from the body.
        l = Fund(funder=funder, option=option,
                 amount=amount, status=Fund.PENDING)
        l.save()
        serializer = FundSerializer(l)

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
            Make sure that only a Banker can change the status of any pending item.
        """
        if request.user.user_type != User.BANKER:
            raise PermissionDenied()

        body = toJSON(request.body)

        # Get the status that'll change
        status = body["status"]
        print("Updating : " + pk)

        """
            Get the fund object to change, change the status and then commit the save.
        """
        fundQS = Fund.objects.filter(pk=pk).prefetch_related('option')
        if len(fundQS) == 0:
            return Response({"Message": "Fund ID incorrect"}, status=HTTPStatus.HTTP_404_NOT_FOUND)
        fund = fundQS[0]

        if status != Fund.APPROVED:
            print("DENIED")
            fund.status = status
            fund.save()
            serializer = FundSerializer(fund)
            return Response(serializer.data)

        product = stripe.Product.create(
            name="fund-" + str(pk) + "-" + str(fund.funder)
        )

        unit_amount = math.ceil(float("{:.2f}".format(fund.amount)))
        price = stripe.Price.create(
            unit_amount=unit_amount * 100,
            currency="usd",
            product=product.id
        )
        print(product)
        print(price)

        # # Get the bank object or create it.
        bank = get_or_create_bank()

        # Add the amount into the bank balance.
        interest_rate = fund.option.interest_rate / 100
        monthly_rate = Decimal(interest_rate / 12)
        monthly_payment_amount = fund.amount * \
            (monthly_rate / (1 - (1+monthly_rate)**(-fund.option.duration)))

        fund_total_outflow = (Decimal(monthly_payment_amount) *
                              int(fund.option.duration)) - Decimal(fund.amount)
        if bank.out_flow + fund_total_outflow >= bank.in_flow:
            return Response({"message": "This fund is not viable since it costs more than the total in flow"}, status=HTTPStatus.HTTP_403_FORBIDDEN)

        fund.payment_url = price.id
        fund.status = status
        fund.save()

        bank.out_flow += fund_total_outflow
        bank.total_amount += fund.amount
        bank.save()
        serializer = FundSerializer(fund)
        return Response(serializer.data)


"""
    Get all funds for a specific funder.
"""


@api_view(['GET'])
def view_funder_funds(request, id):

    if request.user.id != id:
        raise PermissionDenied()

    queryset = Fund.objects.all().filter(funder=id)
    serializer = FundSerializer(queryset, many=True)
    return Response(serializer.data)


"""
    Verify Fund Payment
"""


@api_view(['POST'])
def verify_fund_payment(request, fund_id):
    print(fund_id)
    print(request.user)
    if request.user.user_type != User.FUNDER:
        print("Not a funder")
        raise PermissionDenied()

    payments = stripe.PaymentIntent.list()

    for t in payments:
        print(("fund" + "-" + str(fund_id) + "-" +
               str(request.user)) in t["description"])
        if ("fund" + "-" + str(fund_id) + "-" + str(request.user)) in t["description"]:
            print(t["amount_received"])
            print(t["charges"]["data"][0]["receipt_url"])
            print(t["description"])
            queryset = Fund.objects.all()
            fund = get_object_or_404(queryset, id=fund_id)

            if fund.payment_verified:
                return Response({"message": "Payment Already Verified"}, status=HTTPStatus.HTTP_409_CONFLICT)

            if t["amount_received"] + 1 >= fund.amount:
                fund.payment_verified = True
                fund.payment_receipt_url = t["charges"]["data"][0]["receipt_url"]
                fund.save()

                serializer = FundSerializer(fund)
                return Response(serializer.data)

    return Response({"message": "Couldn't find payment for fund specified"}, status=HTTPStatus.HTTP_404_NOT_FOUND)


"""
    List all the pending funds for the banker.
"""


@api_view(['GET'])
def view_pending_funds(request):
    # Check user is a banker.
    if request.user.user_type != User.BANKER:
        raise PermissionDenied()

    # Get all objects with status PENDING.
    queryset = Fund.objects.all().filter(status=Fund.PENDING)
    serializer = FundSerializer(queryset, many=True)
    return Response(serializer.data)
# git remote add origin https://[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]@github.com/ahmednader42/bank-frontend.git

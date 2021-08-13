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
from decimal import *

# Create your views here.


class FundOptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrReadOnly,)
    queryset = FundOption.objects.all()
    serializer_class = FundOptionSerializer


class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    def create(self, request): 3
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

        """
            Get the fund object to change, change the status and then commit the save.
        """
        fund = get_object_or_404(Fund, pk=pk)
        fund.status = status
        fund.save()

        # Get the bank object or create it.
        bank = get_or_create_bank()

        # Add the amount into the bank balance.
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

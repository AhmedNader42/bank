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
from bank.views import create_bank
from django.shortcuts import get_object_or_404
# Create your views here.


class FundOptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrReadOnly,)
    queryset = FundOption.objects.all()
    serializer_class = FundOptionSerializer


class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    def create(self, request):
        body = toJSON(request.body)

        print(request.user.id)
        print(body['funder'])
        if request.user.id != body['funder'] or request.user.user_type != User.FUNDER:
            raise PermissionDenied()

        funder = User.objects.get(pk=body['funder'])
        amount = body['amount']
        option = FundOption.objects.get(pk=body['option'])

        if amount > option.maximum_amount or amount < option.minimum_amount:
            return Response({"message": "Incorrect amount for your plan"})

        l = Fund(funder=funder, option=option,
                 amount=amount, status=Fund.PENDING)
        l.save()
        serializer = FundSerializer(l)

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        if request.user.user_type != User.BANKER:
            raise PermissionDenied()
        body = toJSON(request.body)
        status = body["status"]

        fund = get_object_or_404(Fund, pk=pk)

        bankList = Bank.objects.all().filter(pk=0)

        bank = None
        if len(bankList) == 0:
            create_bank()
            bankList = Bank.objects.all().filter(pk=0)
            bank = bankList[0]
        else:
            bank = bankList[0]

        fund.status = status
        fund.save()
        bank.total_amount += fund.amount
        bank.save()
        serializer = FundSerializer(fund)
        return Response(serializer.data)


@api_view(['GET'])
def view_funder_funds(request, id):

    if request.user.id != id:
        raise PermissionDenied()

    queryset = Fund.objects.all().filter(funder=id)
    serializer = FundSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_pending_funds(request):
    if request.user.user_type != User.BANKER:
        raise PermissionDenied()

    queryset = Fund.objects.all().filter(status=Fund.PENDING)
    serializer = FundSerializer(queryset, many=True)
    return Response(serializer.data)

from .models import Loan, LoanOption
from rest_framework import viewsets
from .serializers import LoanSerializer, LoanOptionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .permissions import IsBankerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from users.models import User
from .helpers import toJSON
from bank.models import Bank
from bank.views import get_or_create_bank
from django.shortcuts import get_object_or_404
# Create your views here.


class LoanOptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrReadOnly,)
    queryset = LoanOption.objects.all()
    serializer_class = LoanOptionSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request):
        # Parse the body into valid JSON with this helper function.
        body = toJSON(request.body)

        """
            - Make sure that a customer can only add loans for himself.
            - Make sure that the request is done by a customer.
        """
        if request.user.id != body['customer'] or request.user.user_type != User.CUSTOMER:
            raise PermissionDenied()

        # Gather the data from the request body.
        customer = User.objects.get(pk=body['customer'])
        amount = body['amount']
        option = LoanOption.objects.get(pk=body['option'])

        # Make sure the loan amount fits in the range of the loan option
        if amount > option.maximum_amount or amount < option.minimum_amount:
            return Response({"message": "Incorrect amount for your plan"})

        # Save the loan with the data from the body.
        l = Loan(customer=customer, option=option,
                 amount=amount, status=Loan.PENDING)
        l.save()
        serializer = LoanSerializer(l)

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
            Make sure that only a Banker can change the status of any pending item.
        """
        if request.user.user_type != User.BANKER:
            raise PermissionDenied()

        body = toJSON(request.body)

        # Get the status from the request body.
        status = body["status"]

        # Fetch the loan object.
        loan = get_object_or_404(Loan, pk=pk)

        """
            If the item is Denied or Pending then update right away without having to check with the system.
        """
        if status != Loan.APPROVED:
            loan.status = status
            loan.save()
            serializer = LoanSerializer(loan)
            return Response(serializer.data)

        # Get the bank object or create it.
        bank = get_or_create_bank()

        """
            Make sure the bank can loan the customer the amount needed from the bank balance.
        """
        if loan.amount < bank.total_amount:
            print("Can take loan")
            loan.status = status
            loan.save()

            bank.total_amount -= loan.amount
            bank.save()
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        else:
            print("Can't take loan")
            return Response({"message": "Not enough funds"})


@api_view(['GET'])
def view_customer_loans(request, id):

    if request.user.id != id:
        raise PermissionDenied()

    queryset = Loan.objects.all().filter(customer=id)
    serializer = LoanSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_pending_loans(request):
    if request.user.user_type != User.BANKER:
        raise PermissionDenied()

    queryset = Loan.objects.all().filter(status=Loan.PENDING)
    serializer = LoanSerializer(queryset, many=True)
    return Response(serializer.data)

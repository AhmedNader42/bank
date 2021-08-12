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

# Create your views here.


class LoanOptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrReadOnly,)
    queryset = LoanOption.objects.all()
    serializer_class = LoanOptionSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request):
        body = toJSON(request.body)

        if request.user.id != body['customer'] or request.user.user_type != User.CUSTOMER:
            print(request.user.id != body['customer'])
            print(request.user.user_type != User.CUSTOMER)
            raise PermissionDenied

        customer = User.objects.get(pk=body['customer'])
        amount = body['amount']
        loan_type = LoanOption.objects.get(pk=body['loan_type'])

        
        if amount > loan_type.maximum_amount or amount < loan_type.minimum_amount:
            return Response({"message": "Incorrect amount for your plan"})

        l = Loan(customer=customer, loan_type=loan_type,
                 amount=amount, status=Loan.PENDING)
        l.save()
        serializer = LoanSerializer(l)

        return Response(serializer.data)


@api_view(['GET'])
def view_customer_loans(request, id):

    if request.user.id != id and not request.user.is_superuser:
        raise PermissionDenied()

    queryset = Loan.objects.all().filter(customer=id)
    for l in queryset:
        print(l.customer)
    serializer = LoanSerializer(queryset, many=True)
    return Response(serializer.data)

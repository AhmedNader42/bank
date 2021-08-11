from .models import User, Loan
from rest_framework import viewsets
from .serializers import UserSerializer, LoanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .permissions import IsBankerOrAdmin
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
import json


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create your views here.


class LoanViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrAdmin,)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request):
        print("creating")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        customer = User.objects.get(pk=body['customer'])
        amount = body['amount']
        duration = body['duration']
        l = Loan(customer=customer, amount=amount,
                 duration=duration, status=Loan.PENDING)
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

from .models import Loan
from rest_framework import viewsets
from .serializers import LoanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .permissions import IsBankerOrAdmin
from rest_framework.exceptions import PermissionDenied
from users.models import User
from .helpers import toJSON

# Create your views here.


class LoanViewSet(viewsets.ModelViewSet):
    permission_classes = (IsBankerOrAdmin,)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request):
        body = toJSON(request.body)

        if not request.user.is_superuser:
            if request.user.id != body['customer'] or request.user.user_type != User.CUSTOMER:
                raise PermissionDenied

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

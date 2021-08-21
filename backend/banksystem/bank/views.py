from django.shortcuts import render
from .models import Bank
from .serializers import BankSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users.models import User

from funds.models import Fund
from loans.models import Loan

# Create your views here.

"""
    This function checks for the bank object existance and if it doesn't then creates it.
    The Bank balance needs to be a Singelton to all calculations of loans and funds consistent.
"""


def get_or_create_bank():
    if Bank.objects.filter(pk=0).exists():
        print("Exists")
        # In case the bank exists return it
        return Bank.objects.get(pk=0)
    else:
        # In case the bank doesn't exist create it with an initial fund of 10k and return it.
        print("Bank doesn't exist!")
        b = Bank(id=0, total_amount=10000.0, in_flow=0.0, out_flow=0.0)
        # Commit to the database.
        b.save()
        return b


"""
    Make sure only a Banker can view the total_amount of balance in the Bank.
"""


@api_view(['GET'])
def get_total_amount(request):
    # Make sure the user is a Banker to see the bank balance. Otherwise deny permission.
    if request.user.user_type != User.BANKER:
        raise PermissionDenied()

    # Get the bank object
    bank = get_or_create_bank()

    serializer = BankSerializer(bank)
    # Return the total amount for the balance
    return Response(serializer.data)


"""
    Make sure only a Banker can view the total_amount of balance in the Bank.
"""


@api_view(['GET'])
def system_report(request):
    # Make sure the user is a Banker.
    if request.user.user_type != User.BANKER:
        raise PermissionDenied()

    pending_funds = Fund.objects.all().filter(status=Fund.PENDING).count()
    approved_funds = Fund.objects.all().filter(status=Fund.APPROVED).count()
    denied_funds = Fund.objects.all().filter(status=Fund.DENIED).count()

    pending_loans = Loan.objects.all().filter(status=Loan.PENDING).count()
    approved_loans = Loan.objects.all().filter(status=Loan.APPROVED).count()
    denied_loans = Loan.objects.all().filter(status=Loan.DENIED).count()

    number_of_bankers = User.objects.all().filter(user_type=User.BANKER).count()
    number_of_customers = User.objects.all().filter(user_type=User.CUSTOMER).count()
    number_of_funders = User.objects.all().filter(user_type=User.FUNDER).count()

    # Return the total amount for the balance
    return Response({
        "total_number_of_funds": pending_funds + approved_funds + denied_funds,
        "pending_funds": pending_funds,
        "approved_funds": approved_funds,
        "denied_funds": denied_funds,

        "total_number_of_loans": pending_loans + approved_loans + denied_loans,
        "pending_loans": pending_loans,
        "approved_loans": approved_loans,
        "denied_loans": denied_loans,

        "total_number_of_users": number_of_funders + number_of_customers + number_of_bankers,
        "bankers": number_of_bankers,
        "customer": number_of_customers,
        "funders": number_of_funders,
    })

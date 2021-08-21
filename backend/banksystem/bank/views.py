from django.shortcuts import render
from .models import Bank
from .serializers import BankSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from users.models import User

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

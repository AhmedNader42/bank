from django.shortcuts import render
from .models import Bank
from .serializers import BankSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


# Create your views here.
def create_bank():
    b = Bank(id=0, total_amount=0.0)
    b.save()
    print(b)

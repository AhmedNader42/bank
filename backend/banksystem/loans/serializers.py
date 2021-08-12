from rest_framework import serializers
from .models import Loan, LoanOption


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'customer', 'loan_type', 'amount', 'started', 'status')

class LoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOption
        fields = ('id', 'minimum_amount', 'maximum_amount', 'duration', 'interest_rate')

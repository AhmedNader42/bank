from rest_framework import serializers
from .models import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'total_amount', 'in_flow', 'out_flow')

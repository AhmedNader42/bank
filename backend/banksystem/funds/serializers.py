from rest_framework import serializers
from .models import Fund, FundOption


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ('id', 'funder', 'option', 'amount',
                  'started', 'status', 'payment_url', 'payment_verified', 'payment_receipt_url')


class FundOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundOption
        fields = ('id', 'minimum_amount', 'maximum_amount',
                  'duration', 'interest_rate')

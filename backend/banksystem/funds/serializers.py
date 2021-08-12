from rest_framework import serializers
from .models import Fund, FundOption


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ('id', 'funder', 'option', 'amount', 'started', 'status')


class FundOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundOption
        fields = ('id', 'minimum_amount', 'maximum_amount',
                  'duration', 'interest_rate')

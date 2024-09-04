# loans/serializers.py
from rest_framework import serializers
from .models import BaseLoanFund

class BaseLoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseLoanFund
        fields = ['id', 'type', 'start_fund', 'created_at', 'current_value']


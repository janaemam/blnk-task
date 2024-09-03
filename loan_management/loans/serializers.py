# serializers.py
from rest_framework import serializers
from .models import LoanPlan, LoanRequest, Loan, LoanPayment

class LoanPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPlan
        fields = '__all__'

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'

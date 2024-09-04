from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, write_only=True)
    credit_score = serializers.DecimalField(max_digits=10, decimal_places=2, default=800, write_only=True)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, write_only=True)
    age = serializers.IntegerField(write_only=True)
    dependents = serializers.IntegerField(default=0, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'balance',
                  'credit_score', 'salary', 'age', 'dependents')

    def validate(self, data):
        
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})
        return data

    def create(self, validated_data):
      
        balance = validated_data.pop('balance', 0)
        credit_score = validated_data.pop('credit_score', 800)
        salary = validated_data.pop('salary', 0)
        age = validated_data.pop('age')
        dependents = validated_data.pop('dependents', 0)

        
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_customer=True,
        )
        user.set_password(validated_data['password'])
        user.save()

       
        Customer.objects.create(
            user=user,
            balance=balance,
            credit_score=credit_score,
            salary=salary,
            age=age,
            dependents=dependents
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_bank_personnel = models.BooleanField(default=False)
    is_fund_provider = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Avoiding reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit_score = models.DecimalField(max_digits=10, decimal_places=2, default=800)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    age = models.PositiveIntegerField()
    dependents = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.user)

class BankPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

class FundProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

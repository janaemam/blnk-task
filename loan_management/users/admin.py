from django.contrib import admin
from .models import User, Customer, BankPersonnel, FundProvider

admin.site.register(BankPersonnel)

admin.site.register(Customer)
admin.site.register(FundProvider)

admin.site.register(User)
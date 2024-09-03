# urls.py in the users app

from django.urls import path
from django.urls import path
from .views import (
    CustomerRegisterView, 
    LoginView, 
    LogoutView, 
    CustomerHomeView, 
    BankPersonnelHomeView, 
    FundProviderHomeView,
    CheckAuthView
)
urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('customer/home/', CustomerHomeView.as_view(), name='customer-home'),
    path('bank-personnel/home/', BankPersonnelHomeView.as_view(), name='bank-personnel-home'),
    path('fund-provider/home/', FundProviderHomeView.as_view(), name='fund-provider-home'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
]

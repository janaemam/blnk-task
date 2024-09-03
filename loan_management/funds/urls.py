from django.urls import path
from .views import BaseLoanFundViewSet

urlpatterns = [
    path('funds/', BaseLoanFundViewSet.as_view({'get': 'list'}), name='base-loan-fund-list'),
    path('funds/create/', BaseLoanFundViewSet.as_view({'post': 'create'}), name='base-loan-fund-create'),
]

from django.urls import path
from .views import (
    LoanPlanViewSet,
    LoanRequestViewSet,
    LoanViewSet
)

urlpatterns = [
    path('loan-plans/', LoanPlanViewSet.as_view({'get': 'list'}), name='loan-plan-list'),
    path('loan-plans/create/', LoanPlanViewSet.as_view({'post': 'create'}), name='loan-plan-create'),
    path('loan-requests/', LoanRequestViewSet.as_view({'get': 'list'}), name='loan-request-list'),
    path('loan-requests/apply/', LoanRequestViewSet.as_view({'post': 'apply'}), name='loan-request-apply'),
    path('loan-requests/status/', LoanRequestViewSet.as_view({'get': 'status'}), name='loan-request-status'),
    path('loans/', LoanViewSet.as_view({'get': 'list'}), name='loan-list'),
    path('loans/<int:pk>/', LoanViewSet.as_view({'get': 'retrieve'}), name='loan-detail'),
]

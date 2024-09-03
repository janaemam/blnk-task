from rest_framework import viewsets
from .serializers import BaseLoanFundSerializer
from .models import BaseLoanFund
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied

class BaseLoanFundViewSet(viewsets.ModelViewSet):
    serializer_class = BaseLoanFundSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_fund_provider:
            return BaseLoanFund.objects.all()
        else:
            raise PermissionDenied("You do not have permission to view this resource.")

    def perform_create(self, serializer):
        if self.request.user.is_fund_provider:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create a fund.")

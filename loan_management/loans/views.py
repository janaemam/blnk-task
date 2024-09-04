from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LoanPlan, LoanRequest, Loan, LoanPayment
from .serializers import LoanPlanSerializer, LoanRequestSerializer, LoanSerializer, LoanPaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Count
from users.permissions import IsBankPersonnel, IsCustomer

class LoanPlanViewSet(viewsets.ModelViewSet):
    queryset = LoanPlan.objects.all()
    serializer_class = LoanPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsBankPersonnel]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def available_for_customers(self, request):
        """Return all available loan plans for customers."""
        if request.user.is_customer:
            loan_plans = LoanPlan.objects.all()
            serializer = LoanPlanSerializer(loan_plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permission to view loan plans'}, status=status.HTTP_403_FORBIDDEN)


class LoanRequestViewSet(viewsets.ModelViewSet):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'apply':
            permission_classes = [IsAuthenticated, IsCustomer]
        elif self.action in ['approve', 'reject', 'all_loan_requests', 'active_loans']:
            permission_classes = [IsAuthenticated, IsBankPersonnel]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def apply(self, request):
        """Allow customers to apply for a loan."""
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            loan_plan = serializer.validated_data['loan_plan']
            principal = serializer.validated_data['principal']
            loan_request = serializer.save(user=request.user, total=self.calculate_total(principal, loan_plan))
            return Response(LoanRequestSerializer(loan_request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def status(self, request):
        """Allow customers to check the status of their loan requests."""
        loan_requests = LoanRequest.objects.filter(user=request.user)
        serializer = LoanRequestSerializer(loan_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def make_payment(self, request):
        """Allow customers to make payments on their loans."""
        loan_id = request.data.get('loan_id')
        amount = request.data.get('amount')
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        if amount <= 0:
            return Response({"error": "Amount must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        if loan.paid + amount > loan.total:
            return Response({"error": "Payment exceeds the total loan amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        LoanPayment.objects.create(loan=loan, amount=amount, user=request.user)
        loan.paid += amount
        loan.save()
        return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

    def calculate_total(self, principal, loan_plan):
        """Calculate the total amount to be repaid based on the principal and loan plan."""
        interest_rate = loan_plan.interest_rate
        total = principal * (1 + (interest_rate / 100))  
        return total

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a loan request."""
        loan_request = get_object_or_404(LoanRequest, pk=pk)
        if request.user.is_bank_personnel:
            loan_request.request_status = 'APPROVED'
            loan_request.loan_officer = request.user.bankpersonnel
            loan_request.save()
            return Response({'status': 'Loan request approved'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permission to approve loan requests'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a loan request."""
        loan_request = get_object_or_404(LoanRequest, pk=pk)
        if request.user.is_bank_personnel:
            loan_request.request_status = 'REJECTED'
            loan_request.loan_officer = request.user.bankpersonnel
            loan_request.save()
            return Response({'status': 'Loan request rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have permission to reject loan requests'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def all_loan_requests(self, request):
        """Allow bank personnel to view all loan requests."""
        if request.user.is_bank_personnel:
            loan_requests = LoanRequest.objects.all()
            serializer = LoanRequestSerializer(loan_requests, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to view loan requests'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def active_loans(self, request):
        """Allow bank personnel to check all active loans."""
        if request.user.is_bank_personnel:
            loans = Loan.objects.filter(paid__lt=F('total'))
            serializer = LoanSerializer(loans, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to view active loans'}, status=status.HTTP_403_FORBIDDEN)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'])
    def all_active_loans(self, request):
        """Allow fund providers to check all active loans."""
        loans = Loan.objects.filter(paid__lt=F('total'))
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


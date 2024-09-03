# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from django.urls import reverse
# from .models import LoanPlan, LoanRequest, Loan
# from users.models import User, Customer, BankPersonnel
# from funds.models import BaseLoanFund

# class LoanTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
        
#         # Create BankPersonnel and Customer users
#         self.bank_personnel = User.objects.create_user(
#             username='bankpersonnel', password='password123', email='bankpersonnel@example.com', is_bank_personnel=True)
#         self.customer = User.objects.create_user(
#             username='customer', password='password123', email='customer@example.com', is_customer=True)
        
#         # Create Customer profile
#         self.customer_profile = Customer.objects.create(
#             user=self.customer, balance=1000, credit_score=750, salary=5000, age=30)
       
#         self.bank_personnel_profile = BankPersonnel.objects.create(user=self.bank_personnel)

#         # Create BaseLoanFund and LoanPlan
#         self.fund = BaseLoanFund.objects.create(type='BIG', start_fund=100000, current_value=100000)
#         self.loan_plan = LoanPlan.objects.create(
#             loan_fund=self.fund, name='Standard Loan', interest_rate=5, max_value=50000, min_value=300, duration=12)
        
#         # Define URLs for testing
#         self.loan_request_url = reverse('loan-request-apply')
#         self.loan_url = reverse('loan-list')

#     def test_loan_request(self):
#         self.client.force_authenticate(user=self.customer)
#         data = {
#             'loan_plan': self.loan_plan.id,
#             'principal': 5000,
#             'total': 5250,  # Principal + 5% interest
#             'request_status': 'PENDING'  # Assuming default is pending
#         }
#         response = self.client.post(self.loan_request_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(LoanRequest.objects.count(), 1)

#     def test_loan_creation(self):
#         # Create a LoanRequest instance with approved status
#         loan_request = LoanRequest.objects.create(
#             loan_plan=self.loan_plan,
#             user=self.customer_profile,
#             principal=5000,
#             total=5250,  # Principal + 5% interest
#             request_status='APPROVED',
#             loan_officer=self.bank_personnel_profile  # Use BankPersonnel instance here
#         )
        
#         self.client.force_authenticate(user=self.bank_personnel)
#         data = {
#             'loan_request': loan_request.id
#         }
#         response = self.client.post(self.loan_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Loan.objects.count(), 1)
#         self.assertEqual(response.data['total'], 5250)  # Total loan amount

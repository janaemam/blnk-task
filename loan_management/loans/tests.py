from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LoanPlan, LoanRequest, Loan, LoanPayment
from funds.models import BaseLoanFund
from users.models import Customer, BankPersonnel
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import LoanPlan, LoanRequest, Loan, LoanPayment
from funds.models import BaseLoanFund
from users.models import User, Customer, BankPersonnel


User = get_user_model()

class BaseLoanFundModelTest(TestCase):
    def test_create_base_loan_fund(self):
        fund = BaseLoanFund.objects.create(
            type='BIG', 
            start_fund=1000000, 
            current_value=1000000
        )
        self.assertEqual(fund.type, 'BIG')
        self.assertEqual(fund.start_fund, 1000000)
        self.assertEqual(fund.current_value, 1000000)
        self.assertIsNotNone(fund.created_at)

class LoanPlanModelTest(TestCase):
    def test_create_loan_plan(self):
        fund = BaseLoanFund.objects.create(
            type='MEDIUM', 
            start_fund=500000, 
            current_value=500000
        )
        loan_plan = LoanPlan.objects.create(
            name='Home Loan', 
            loan_fund=fund, 
            interest_rate=5.0, 
            min_value=10000, 
            max_value=50000, 
            duration=12
        )
        self.assertEqual(loan_plan.name, 'Home Loan')
        self.assertEqual(loan_plan.loan_fund, fund)
        self.assertEqual(loan_plan.interest_rate, 5.0)
        self.assertEqual(loan_plan.min_value, 10000)
        self.assertEqual(loan_plan.max_value, 50000)
        self.assertEqual(loan_plan.duration, 12)

class LoanRequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', 
            password='testpassword',
            email='customer@example.com',
            is_customer=True
        )
        self.customer = Customer.objects.create(user=self.user, age=30, salary=3000)
        self.fund = BaseLoanFund.objects.create(
            type='SMALL', 
            start_fund=100000, 
            current_value=100000
        )
        self.loan_plan = LoanPlan.objects.create(
            name='Personal Loan', 
            loan_fund=self.fund, 
            interest_rate=10.0, 
            min_value=5000, 
            max_value=20000, 
            duration=6
        )

    def test_create_loan_request(self):
        loan_request = LoanRequest.objects.create(
            loan_plan=self.loan_plan, 
            user=self.customer, 
            principal=5000, 
            total=5500, 
            request_status='PENDING'
        )
        self.assertEqual(loan_request.loan_plan, self.loan_plan)
        self.assertEqual(loan_request.user, self.customer)
        self.assertEqual(loan_request.principal, 5000)
        self.assertEqual(loan_request.total, 5500)
        self.assertEqual(loan_request.request_status, 'PENDING')

class LoanModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', 
            password='testpassword',
            email='customer@example.com',
            is_customer=True
        )
        self.customer = Customer.objects.create(user=self.user, age=30, salary=3000)
        self.fund = BaseLoanFund.objects.create(
            type='SMALL', 
            start_fund=100000, 
            current_value=100000
        )
        self.loan_plan = LoanPlan.objects.create(
            name='Personal Loan', 
            loan_fund=self.fund, 
            interest_rate=10.0, 
            min_value=5000, 
            max_value=20000, 
            duration=6
        )
        self.loan_request = LoanRequest.objects.create(
            loan_plan=self.loan_plan, 
            user=self.customer, 
            principal=5000, 
            total=5500, 
            request_status='PENDING'
        )

    def test_create_loan(self):
        loan = Loan.objects.create(
            loan_plan=self.loan_plan, 
            user=self.customer, 
            paid=0, 
            total=5500
        )
        self.assertEqual(loan.loan_plan, self.loan_plan)
        self.assertEqual(loan.user, self.customer)
        self.assertEqual(loan.paid, 0)
        self.assertEqual(loan.total, 5500)

class LoanPaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', 
            password='testpassword',
            email='customer@example.com',
            is_customer=True
        )
        self.customer = Customer.objects.create(user=self.user, age=30, salary=3000)
        self.fund = BaseLoanFund.objects.create(
            type='SMALL', 
            start_fund=100000, 
            current_value=100000
        )
        self.loan_plan = LoanPlan.objects.create(
            name='Personal Loan', 
            loan_fund=self.fund, 
            interest_rate=10.0, 
            min_value=5000, 
            max_value=20000, 
            duration=6
        )
        self.loan = Loan.objects.create(
            loan_plan=self.loan_plan, 
            user=self.customer, 
            paid=0, 
            total=5500
        )

    def test_create_loan_payment(self):
        payment = LoanPayment.objects.create(
            loan=self.loan, 
            amount=1000, 
            user=self.customer
        )
        self.assertEqual(payment.loan, self.loan)
        self.assertEqual(payment.amount, 1000)
        self.assertEqual(payment.user, self.customer)
        self.assertIsNotNone(payment.paid_at)


class LoanPlanViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='personnel', 
            password='testpassword',
            email='personnel@example.com',
            is_bank_personnel=True
        )
        self.bank_personnel = BankPersonnel.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.fund = BaseLoanFund.objects.create(
            type='MEDIUM', 
            start_fund=500000, 
            current_value=500000
        )
        self.loan_plan_data = {
            'name': 'Car Loan',
            'loan_fund': self.fund.id,
            'interest_rate': 7.0,
            'min_value': 10000,
            'max_value': 30000,
            'duration': 24
        }

    def test_create_loan_plan(self):
        response = self.client.post(reverse('loan-plan-create'), self.loan_plan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanPlan.objects.count(), 1)
        self.assertEqual(LoanPlan.objects.get().name, 'Car Loan')

    def test_list_loan_plans(self):
       
        self.loan_plan_data['loan_fund'] = self.fund
        LoanPlan.objects.create(**self.loan_plan_data)
        
        response = self.client.get(reverse('loan-plan-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class LoanRequestViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', 
            password='testpassword',
            email='customer@example.com',
            is_customer=True
        )
        self.customer = Customer.objects.create(user=self.user, age=30, salary=3000)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Auth as customer
        self.fund = BaseLoanFund.objects.create(
            type='SMALL', 
            start_fund=100000, 
            current_value=100000
        )
        self.loan_plan = LoanPlan.objects.create(
            name='Personal Loan', 
            loan_fund=self.fund, 
            interest_rate=10.0, 
            min_value=5000, 
            max_value=20000, 
            duration=6
        )
        self.loan_request_data = {
            'loan_plan': self.loan_plan.id,  # Ensure correct ID is passed
            'principal': 5000,
            'total': 5500,
            'request_status': 'PENDING'
        }
def test_check_loan_request_status(self):
   
    loan_request = LoanRequest.objects.create(
        loan_plan=self.loan_plan, 
        user=self.customer,  
        principal=5000, 
        total=5500, 
        request_status='PENDING'
    )
    self.client.force_login(self.customer.user)

    url = reverse('loan-request-status')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['principal'], loan_request.principal)
    self.assertEqual(response.data['total'], loan_request.total)
    self.assertEqual(response.data['request_status'], loan_request.request_status)
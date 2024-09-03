from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import BaseLoanFund
from users.models import User

class BaseLoanFundTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.fund_provider = User.objects.create_user(
            username='fundprovider', email='fundprovider@example.com', password='password123', is_fund_provider=True)
        self.fund_url = reverse('base-loan-fund-create')

    def test_create_fund(self):
        self.client.force_authenticate(user=self.fund_provider)
        data = {
            'type': 'BIG',
            'start_fund': 100000,
            'current_value': 100000
        }
        response = self.client.post(self.fund_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BaseLoanFund.objects.count(), 1)

    def test_fund_list_permission(self):
        self.client.force_authenticate(user=self.fund_provider)
        response = self.client.get(reverse('base-loan-fund-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test with a non-fund provider user
        non_fund_provider = User.objects.create_user(
            username='customer', email='customer@example.com', password='password123', is_customer=True)
        self.client.force_authenticate(user=non_fund_provider)
        response = self.client.get(reverse('base-loan-fund-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

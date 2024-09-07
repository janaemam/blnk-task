from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Customer
from rest_framework.authtoken.models import Token

class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('customer-register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'balance': 1000,
            'credit_score': 750,
            'salary': 5000,
            'age': 30,
            'dependents': 2
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='password123', is_customer=True)
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'customer')

    def test_user_logout(self):
        user = User.objects.create_user(username='testuser', password='password123', is_customer=True)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ token.key)
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=user).exists())


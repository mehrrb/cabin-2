from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account
from django.contrib.contenttypes.models import ContentType
from cabin.models import Rider, Driver

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a rider and driver for testing
        self.rider = Rider.objects.create(rating=4.5, x=35.0, y=45.0)
        self.driver = Driver.objects.create(rating=4.8, x=35.0, y=45.0, active=True)
        
        # Create an account for login testing
        self.user = Account.objects.create_user(
            phone='09123456789',
            email='test@example.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        self.user.content_type = ContentType.objects.get_for_model(Rider)
        self.user.object_id = self.rider.id
        self.user.save()

    def test_register_success(self):
        """
        Test successful registration of a new user
        """
        url = reverse('register')
        data = {
            'phone': '09187654321',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertEqual(Account.objects.count(), 2)

    def test_register_duplicate_phone(self):
        """
        Test registration with duplicate phone number
        """
        url = reverse('register')
        data = {
            'phone': '09123456789',  # Duplicate phone number
            'email': 'another@example.com',
            'password': 'test123',
            'first_name': 'Another',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Test successful login
        """
        url = reverse('login')
        data = {
            'phone': '09123456789',
            'password': 'test123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials
        """
        url = reverse('login')
        data = {
            'phone': '09123456789',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """
        Test successful logout
        """
        # First login
        login_url = reverse('login')
        login_data = {
            'phone': '09123456789',
            'password': 'test123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['tokens']['refresh']

        # Now logout
        logout_url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["tokens"]["access"]}')
        logout_data = {'refresh': refresh_token}
        response = self.client.post(logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_missing_fields(self):
        """
        تست ثبت‌نام با فیلدهای ناقص
        """
        url = reverse('register')
        data = {
            'phone': '09187654321',
            'password': 'newpass123'
            # email و first_name و last_name حذف شده‌اند
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        """
        تست لاگین با فیلدهای ناقص
        """
        url = reverse('login')
        data = {
            'phone': '09123456789'
            # password حذف شده
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh(self):
        """
        تست تجدید توکن
        """
        # اول لاگین می‌کنیم
        login_url = reverse('login')
        login_data = {
            'phone': '09123456789',
            'password': 'test123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['tokens']['refresh']

        # حالا توکن را تجدید می‌کنیم
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

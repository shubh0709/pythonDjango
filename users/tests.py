# tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.phone_number = '1234567890'
        self.otp = '123456'
        self.user = User.objects.create_user(phone_number=self.phone_number)

    def test_registration_with_valid_otp(self):
        url = reverse('register')
        data = {
            'phone_number': self.phone_number,
            'otp': self.otp,
            'employment_history': 'Test Employment History',
            'education': 'Test Education',
            'skills': 'Test Skills'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_registration_with_invalid_otp(self):
        url = reverse('register')
        data = {
            'phone_number': self.phone_number,
            'otp': '654321',
            'employment_history': 'Test Employment History',
            'education': 'Test Education',
            'skills': 'Test Skills'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.json())

    def test_login_with_valid_otp(self):
        url = reverse('login')
        data = {
            'phone_number': self.phone_number,
            'otp': self.otp
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_login_with_invalid_otp(self):
        url = reverse('login')
        data = {
            'phone_number': self.phone_number,
            'otp': '654321'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.json())

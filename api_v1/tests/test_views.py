import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import BankingUser


class BankingUserActions(APITestCase):
    def setUp(self):
        """add dummy user."""
        self.client.post(
            '/api/v1/auth/register/',
            {
                'email': 'janeharry@example.com',
                'date_of_birth': '1994-1-1',
                'national_id': '8988192',
                'first_name': 'Jane',
                'last_name': 'Harry'
            },
            format='json'
        )
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'

    def test_register_user(self):
        """Test registration of new user."""
        user_dict = {
            'email': 'matt@example.com',
            'date_of_birth': '1990-01-01',
            'national_id': '071238281',
            'first_name': 'Matt',
            'last_name': 'Harry'
        }
        response = self.client.post(
            self.register_url, user_dict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = BankingUser.objects.get(email='matt@example.com')
        self.assertDictEqual(created_user.to_dict(), user_dict)

    def test_user_login(self):
        response = self.client.post(self.login_url,
                                    {'email': 'janeharry@example.com',
                                     'password': '8988192'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class BankAccountTestCase(APITestCase):
    def setUp(self):
        self.date_of_birth = datetime.datetime(1990, 1, 1)
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.verify_url = '/api/v1/auth/verify/'
        self.post_account_url = '/api/v1/account/'
        self.user = BankingUser.objects.create_user(
            email='matt@example.com',
            date_of_birth=self.date_of_birth,
            national_id='071238281'
        )

        user_verify_dict = {
            'email': self.user.email,
            'old_password': self.user.national_id,
            'new_password': 'pass123',
        }

        user_login_dict = {
            'email': self.user.email,
            'password': 'pass123',
        }

        self.client.post(self.verify_url, user_verify_dict, format='json')
        response = self.client.post(
            self.login_url, user_login_dict, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_create_bank_account(self):
        account_create_dict = {
            'owner': self.user.id,
            'account_type': 'savings'
        }
        response = self.client.post(
            self.post_account_url, account_create_dict
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

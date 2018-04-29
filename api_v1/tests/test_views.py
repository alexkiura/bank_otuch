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

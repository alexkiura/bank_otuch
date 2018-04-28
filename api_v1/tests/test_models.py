from django.test import TestCase  # noqa: F401
from ..models import BankingUser
from django.db import IntegrityError


class BankingUserTestCase(TestCase):
    def setUp(self):
        self.test_user = BankingUser.objects.create_user(
            email='test_user@example.com')

    def test_creating_banking_user(self):
        current_users = BankingUser.objects.count()
        BankingUser.objects.create_user(email='new_user@example.com')
        self.assertEqual(BankingUser.objects.count(), current_users + 1)
        new_user = BankingUser.objects.last()
        self.assertEqual(new_user.email, 'new_user@example.com')

    def test_can_not_create_duplicates(self):
        BankingUser.objects.create_user(email='new_user@example.com')
        with self.assertRaises(IntegrityError):
            BankingUser.objects.create_user(email='new_user@example.com')

    def test_banking_user_verification(self):
        """
        Tests the verification of a user by taking an unverified_user and
        verifying them.
        """
        self.assertTrue(self.test_user.is_verified)
        self.test_user.verify()
        verified_user = BankingUser.objects.create_user(
            email='test_user@example.com')
        self.assertTrue(verified_user.is_verified)

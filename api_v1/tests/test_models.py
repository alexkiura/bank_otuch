from django.test import TestCase  # noqa: F401
from ..models import BankingUser
from django.db import IntegrityError

import datetime


class BankingUserTestCase(TestCase):
    def setUp(self):
        self.date_of_birth = datetime.datetime(1990, 1, 1)
        self.test_user = BankingUser.objects.create_user(
            email='test_user@example.com',
            date_of_birth=self.date_of_birth,
            national_id='627818'
        )

    def test_creating_banking_user(self):
        current_users = BankingUser.objects.count()
        BankingUser.objects.create_user(
            email='new_user@example.com',
            date_of_birth=self.date_of_birth,
            national_id='123456'
        )
        self.assertEqual(BankingUser.objects.count(), current_users + 1)
        new_user = BankingUser.objects.last()
        self.assertEqual(new_user.email, 'new_user@example.com')
        self.assertEqual(new_user.national_id, '123456')

    def test_can_not_create_duplicate_email(self):
        BankingUser.objects.create_user(
            email='new_user@example.com',
            date_of_birth=self.date_of_birth,
            national_id='78872194'
        )
        with self.assertRaises(IntegrityError):
            BankingUser.objects.create_user(
                email='new_user@example.com',
                date_of_birth=self.date_of_birth,
                national_id='745171'
            )

    def test_can_not_create_duplicate_national_id(self):
        BankingUser.objects.create_user(
            email='new_user32@example.com',
            date_of_birth=self.date_of_birth,
            national_id='78872194'
        )
        with self.assertRaises(IntegrityError):
            BankingUser.objects.create_user(
                email='test_user32@example.com',
                date_of_birth=self.date_of_birth,
                national_id='78872194'
            )

    def test_banking_user_verification(self):
        """
        Tests the verification of a user by taking an unverified_user and
        verifying them.
        """
        self.assertFalse(self.test_user.is_verified)
        self.test_user.verify()
        verified_user = BankingUser.objects.get(
            email='test_user@example.com')
        self.assertTrue(verified_user.is_verified)

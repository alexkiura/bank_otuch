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
        """
        Tests creation of a banking user.
        """
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
        """
        Tests that an exception is raised when
        duplidate email is provided.
        """
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
        """
        Tests that an exception is raised when
        duplidate national_id is provided.
        """
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
        self.test_user.verify(self.test_user.national_id, 'pass123')
        verified_user = BankingUser.objects.get(
            email='test_user@example.com')
        self.assertTrue(verified_user.is_verified)

    def test_create_user_with_no_email(self):
        """
        Tests that an exception is raised when enail is not provided.
        """
        with self.assertRaises(ValueError):
            BankingUser.objects.create_user(
                date_of_birth=self.date_of_birth,
                national_id='7910192'
            )

    def test_create_user_with_no_national_id(self):
        """
        Tests that an exception is raised when national_id is not provided.
        """
        with self.assertRaises(ValueError):
            BankingUser.objects.create_user(
                email='user@example.com',
                date_of_birth=self.date_of_birth,
            )

    def test_create_user_with_no_date_of_birth(self):
        """
        Tests that an exception is raised when date of birth is not provided.
        """
        with self.assertRaises(ValueError):
            BankingUser.objects.create_user(
                email='user@example.com',
                national_id='45261782'
            )

    def test_create_super_user(self):
        """
        Tests creation of a superuser.
        """
        BankingUser.objects.create_superuser(
            email='admin@banking.com',
            national_id='3239019',
            date_of_birth=self.date_of_birth,
        )
        super_user = BankingUser.objects.get(email='admin@banking.com')
        self.assertTrue(super_user.is_superuser)

    def test_create_a_non_staff_super_user(self):
        """
        Tests that an exception is raised when is_staff=False.
        """
        with self.assertRaises(ValueError):
            BankingUser.objects.create_superuser(
                email='admin2@banking.com',
                national_id='3039019',
                date_of_birth=self.date_of_birth,
                is_staff=False
            )

    def test_create_a_non_super_user(self):
        """
        Tests that an exception is raised when is_superuser=False.
        """
        with self.assertRaises(ValueError):
            BankingUser.objects.create_superuser(
                email='admin2@banking.com',
                national_id='3039019',
                date_of_birth=self.date_of_birth,
                is_staff=True,
                is_superuser=False
            )

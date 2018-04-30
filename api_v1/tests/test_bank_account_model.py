import datetime

from django.test import TestCase  # noqa: F401
from ..models import BankAccount, BankingUser


class BankAccountTestCase(TestCase):
    def setUp(self):
        self.date_of_birth = datetime.datetime(1990, 1, 1)
        self.user = BankingUser.objects.create_user(
            email='test_user@example.com',
            date_of_birth=self.date_of_birth,
            national_id='627818'
        )
        self.bank_account = BankAccount.objects.create(
            owner=self.user,
            account_type='current'
        )

    def test_create_bank_account(self):
        bank_account = BankAccount.objects.create(
            owner=self.user,
            account_type='current'
        )
        self.assertEqual(bank_account.owner, self.user)
        self.assertEqual(bank_account.account_type, 'current')

    def test_bank_account_deposit(self):
        self.assertEqual(self.bank_account.balance, 0.00)
        self.bank_account.deposit(10000)
        self.assertEqual(self.bank_account.balance, float(10000))

    def test_bank_account_withdrawal(self):
        self.assertEqual(self.bank_account.balance, 0.00)
        self.bank_account.deposit(100000)
        self.bank_account.withdraw(20000)
        self.assertEqual(self.bank_account.balance, float(80000))

    def test_withdrawal_beyond_daily_limit(self):
        """
        Test that an exception is raised when a withdrawal of more than 100000
        is made.
        """
        self.bank_account.deposit(100000)
        with self.assertRaises(ValueError):
            self.bank_account.withdraw(60000)

    def test_withdrawal_beyond_available_balance(self):
        """
        Test that an exception is raised when a withdrawal exceeds available
        balance.
        """
        self.bank_account.deposit(5000)
        with self.assertRaises(ValueError):
            self.bank_account.withdraw(20000)

    def test_deposit_amount_negative_number(self):
        """
        Test that an exception is raised when a deposit has a negative number.
        """
        with self.assertRaises(ValueError):
            self.bank_account.deposit(-20000)

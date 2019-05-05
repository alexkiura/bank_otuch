from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **fields):
        """
        Create and save a user with the given email and national_idself.
        Use the national_id to set the initial password.
        The user will get a prompt tp update their password on log in.
        """
        email = fields.get('email')
        national_id = fields.get('national_id')
        date_of_birth = fields.get('date_of_birth')
        if not email:
            raise ValueError("Email address is required")
        if not national_id:
            raise ValueError("National Id Number is required")
        if not date_of_birth:
            raise ValueError("Date of birth is required")

        email = self.normalize_email(email)
        user = self.model(**fields)
        # set the national_id as the temporary password
        user.set_one_time_password(national_id)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        fields.setdefault('is_staff', False)
        fields.setdefault('is_superuser', False)
        return self._create_user(**fields)

    def create_superuser(self, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)

        if fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**fields)


class BankingUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=False, unique=False)
    physical_address = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)
    proof_of_address = models.FileField(
        upload_to='files/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'national_id', 'date_of_birth'
    ]
    objects = UserManager()

    @property
    def is_verified(self):
        return self.verified

    def verify(self, old_password, new_password):
        """
        verify a user account.
        An account is verified after the user has updated their password
        """
        if self.check_password(old_password):
            self.set_password(new_password)
            self.verified = self.check_password(new_password)
            self.save()
            return self.is_verified
        else:
            raise ValueError('Incorrect password')

    def set_one_time_password(self, temporary_password):
        """
        Set a temporary password.
        """
        self.set_password(temporary_password)
        self.save()

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'national_id': self.national_id,
            'date_of_birth': str(self.date_of_birth)
        }


class BankAccount(models.Model):
    type_choices = (
        ('savings', 'Savings'),
        ('current', 'Current'),
    )
    owner = models.ForeignKey(
        BankingUser,
        on_delete=models.CASCADE,
        blank=False,
        related_name='accounts')
    account_type = models.CharField(
        max_length=100, choices=type_choices, null=False)
    balance = models.FloatField(default=0, blank=True)
    active = models.BooleanField(default=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def deposit(self, amount):
        amount = float(amount)
        if amount > 0.0:
            self.balance += amount
            self.save()
            return True
        else:
            raise ValueError('Amount needs to be a positive number')

    def withdraw(self, amount):
        amount = float(amount)
        if amount > self.balance:
            raise ValueError('Amount exceeds available balance')
            return False
        if abs(amount) > 50000:
            raise ValueError('Can not withdraw more than 50,000 in one day')
            return False
        else:
            self.balance -= abs(amount)
            self.save()
            return True


class Transaction(models.Model):
    transaction_type_choices = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw')
    )
    timestamp = models.DateTimeField(auto_now=True)
    amount = models.FloatField(default=0, blank=True)
    #     max_digits=15,
    #     decimal_places=2,
    #     default=0.00,
    #     blank=True
    # )
    transaction_type = models.CharField(
        max_length=100,
        choices=transaction_type_choices,
        blank=False,
        null=False
    )
    description = models.CharField(max_length=255, blank=False)
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        blank=False,
        related_name='transactions'
    )
    success = models.BooleanField(default=False, blank=True)


@receiver(post_save, sender=Transaction)
def update_bank_account_balance(sender, **kwargs):
    transaction = kwargs.get('instance')
    created = kwargs.get('created')
    if not created:
        return
    bank_account = transaction.account
    successful = False
    if bank_account:
        if transaction.transaction_type == 'deposit':
            successful = bank_account.deposit(transaction.amount)
        if transaction.transaction_type == 'withdraw':
            successful = bank_account.withdraw(transaction.amount)
    transaction.success = successful
    transaction.save()

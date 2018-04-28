from django.db import models  # noqa: F401
from django.contrib.auth.models import AbstractUser


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
    REQUIRED_FIELDS = ['first_name', 'last_name', 'id_number', 'date_of_birth']

    @property
    def is_verified(self):
        return self.verified

    def verify(self):
        self.verified = True
        self.save()

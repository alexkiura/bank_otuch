from django.contrib import admin  # noqa: F401

from .models import BankingUser


admin.site.register(BankingUser)

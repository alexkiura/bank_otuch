from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import BankingUser, BankAccount, Transaction


class BankingUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    national_id = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate(self, data):
        try:
            validate_email(data['email'])
            super().validate(data)
            return data
        except ValidationError as error:
            raise serializers.ValidationError(error.message)

    class Meta:
        model = BankingUser
        fields = ('date_of_birth', 'email', 'national_id', 'first_name',
                  'last_name')


class BankingUserVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    old_password = serializers.CharField(
        max_length=100, required=True, write_only=True)
    new_password = serializers.CharField(
        max_length=100, required=True, write_only=True)


class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ('__all__')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import BankingUser


class BankingUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    national_id = serializers.EmailField(max_length=100, required=True)
    date_of_birth = serializers.DateField(required=True)

    def validate(self, data):
        try:
            validate_email(data['email'])
            return data
        except ValidationError:
            raise serializers.ValidationError('The email is invalid.')

    class Meta:
        model = BankingUser
        fields = ('date_of_birth', 'email', 'national_id')

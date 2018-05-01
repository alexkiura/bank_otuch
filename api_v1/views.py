from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import BankingUser, BankAccount, Transaction
from .serializers import (BankingUserSerializer, BankingUserVerifySerializer,
                          BankAccountSerializer, TransactionSerializer)
from .utils import send_mail


class BankingUserCreateViewSet(viewsets.ModelViewSet):
    """
    API View that receives a POST with the following fields:
        - email
        - date of birth
        - national id
    Returns a one-time password that can be used for authenticated requests..
    """

    queryset = BankingUser.objects.all().order_by('-date_joined')
    serializer_class = BankingUserSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def send_one_time_password(user):
        name = user.first_name
        password = user.national_id
        email_to = user.email
        verify_url = 'https://bank-otuch.herokuapp.com/api/v1/auth/verify/'
        subject = 'Please verify your account'
        email_from = 'noreply@bank-otuch.com'
        content = (f'Hello {name}. Welcome to Bank Otuch.'
                   f'Your one time password is: {password}.'
                   f'Visit {verify_url} to verify your account'
                   f' and change your password.')
        return send_mail(
            email_to=email_to,
            email_from=email_from,
            content=content,
            subject=subject
        )

    def create(self, request):
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        national_id = request.data.get('national_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            banking_user = BankingUser.objects.create_user(
                email=email,
                date_of_birth=date_of_birth,
                national_id=national_id,
                first_name=first_name,
                last_name=last_name
            )
            if banking_user:  # send one-time password to user
                self.send_one_time_password(user=banking_user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error':
                             serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class BankingUserVerifyViewSet(BankingUserCreateViewSet):
    """
    API View that receives a POST with the following fields:
        - email
        - one time password
    Verifies a user and returns a success messsage..
    """
    serializer_class = BankingUserVerifySerializer

    def verify(self, request):
        email = request.data.get('email')
        one_time_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error':
                             serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            unverified_user = BankingUser.objects.get(email=email)
            unverified_user.verify(one_time_password, new_password)
            return Response({
                    'email': email,
                    'verified': unverified_user.is_verified
                },
                status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'error': [error.args]},
                status=status.HTTP_400_BAD_REQUEST
            )


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        owner = request.user
        account_type = request.data.get('account_type')

        bank_account = BankAccount.objects.create(
            owner=owner, account_type=account_type
        )
        serializer = self.get_serializer(bank_account)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        transactions = Transaction.objects.filter(
            account__owner=request.user).all()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    def do_transact(self, request):
        amount = request.data.get('amount')
        transaction_type = request.data.get('transaction_type')
        account_id = request.data.get('account')
        description = request.data.get('description')
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error':
                             serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            account = BankAccount.objects.get(id=account_id)
            transaction = Transaction.objects.create(
                amount=amount,
                transaction_type=transaction_type,
                account=account,
                description=description
            )
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({
                'error': [error.args]},
                status=status.HTTP_400_BAD_REQUEST
            )

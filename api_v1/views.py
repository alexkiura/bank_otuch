from django.shortcuts import render  # noqa: F401
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BankingUser
from .serializers import BankingUserSerializer, BankingUserVerifySerializer


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

    def create(self, request):
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        national_id = request.data.get('national_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            BankingUser.objects.create_user(
                email=email,
                date_of_birth=date_of_birth,
                national_id=national_id,
                first_name=first_name,
                last_name=last_name
            )
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

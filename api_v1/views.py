from django.shortcuts import render  # noqa: F401
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BankingUser
from .serializers import BankingUserSerializer


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

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            BankingUser.objects.create_user(
                email=email,
                date_of_birth=date_of_birth,
                national_id=national_id
            )
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error':
                             'The email was not valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

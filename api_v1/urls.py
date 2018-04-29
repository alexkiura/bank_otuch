from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import BankingUserCreateViewSet, BankingUserVerifyViewSet

urlpatterns = [
    path(
        'auth/register/',
        BankingUserCreateViewSet.as_view({'post': 'create'}),
        name='user-register'
    ),
    path(
        'auth/verify/',
        BankingUserVerifyViewSet.as_view({'post': 'verify'}),
        name='user-verify'
    ),
    path('auth/login/', obtain_jwt_token, name='user-verify')
]

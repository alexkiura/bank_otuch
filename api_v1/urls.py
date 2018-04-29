from django.urls import path
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
    )
]

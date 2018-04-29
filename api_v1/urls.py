from django.urls import path
from .views import BankingUserCreateViewSet


urlpatterns = [
    path(
        'auth/register/',
        BankingUserCreateViewSet.as_view({'post': 'create'}),
        name='user-register'
    )
]

from django.urls import path , include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserView , CustomJwtTokenObtainView

urlpatterns = [
    path('register',RegisterUserView.as_view(), name="register-user"),
    path('login', CustomJwtTokenObtainView.as_view(), name='login-token'),
    path('refresh', TokenRefreshView.as_view(), name='token-refresh')
]
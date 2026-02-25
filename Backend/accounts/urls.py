from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, MeView

urlpatterns = [
    path("signup", SignupView.as_view()),
    path("login", TokenObtainPairView.as_view()),     # {email, password}로 토큰 발급
    path("refresh", TokenRefreshView.as_view()),
    path("me", MeView.as_view()),
]

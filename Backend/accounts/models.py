from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # username 대신 email로 로그인하고 싶으면 아래처럼 정리 가능
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # admin 생성/표시용

    def __str__(self):
        return self.email

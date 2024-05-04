from django.db import models
import random

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
# from operations.models import PaymentOfLab

import math


def generate_activation_code():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    code = models.CharField(max_length=6, default=generate_activation_code)


class UserManager(BaseUserManager):
    def create_user(self,  email, password=None):
        if email is None:
            raise TypeError('User should have a email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email, password=None):
        if password is None:
            raise TypeError('User should have a password')
        user = self.create_user(email, password)
        user.is_superuser = True
        # user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255,  null=False, blank=True)
    last_name = models.CharField(max_length=255,  null=False, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email} {self.first_name} {self.last_name}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def refresh_tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)

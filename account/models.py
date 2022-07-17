from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import UserManager


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    is_seller = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

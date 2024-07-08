from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import AccountManager
import datetime

class Account(AbstractBaseUser):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    objects = AccountManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.user_id

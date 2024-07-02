import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.UUIDField(unique=True)
  pw = models.CharField(max_length=20)
  name = models.CharField(max_length=20)
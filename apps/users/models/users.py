from django.contrib.auth.models import AbstractUser
from django.db import models
from .roles import Role

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
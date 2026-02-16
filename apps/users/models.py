from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) # e.g., 'Admin', 'Farmer', 'Vet'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15, blank=True)


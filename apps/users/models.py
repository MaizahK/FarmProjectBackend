from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) # e.g., 'Admin', 'Farmer', 'Vet'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255) # e.g., '/api/animals/'
    method = models.CharField(max_length=10, choices=[
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), 
        ('PATCH', 'PATCH'), ('DELETE', 'DELETE')
    ])

    class Meta:
        unique_together = ('path', 'method')

    def __str__(self):
        return f"{self.method} {self.path}"

class RolePermissionMapping(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15, blank=True)


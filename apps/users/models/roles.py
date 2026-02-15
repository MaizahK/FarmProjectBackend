from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) # e.g., 'Admin', 'Farmer', 'Vet'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
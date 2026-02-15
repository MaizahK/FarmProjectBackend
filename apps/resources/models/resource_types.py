from django.db import models

class ResourceType(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "Vaccine", "Feed"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


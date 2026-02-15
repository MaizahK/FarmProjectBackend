from django.db import models
from .resource_types import ResourceType

class Resource(models.Model):
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200) # e.g., "Foot & Mouth Vax v2"
    vendor = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.resource_type.name})"
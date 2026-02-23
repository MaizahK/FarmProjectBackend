from django.db import models
    
class ResourceType(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "Vaccine", "Feed"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200) # e.g., "Polio, Grass"
    quantity = models.CharField(max_length=200, blank=True)
    vendor = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.resource_type.name})"


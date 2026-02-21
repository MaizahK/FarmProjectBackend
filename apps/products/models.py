from django.db import models
    
class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "Vaccine", "Feed"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, blank=True)
    quantity = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name} ({self.product_type.name})"


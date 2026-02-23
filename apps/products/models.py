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
    animal = models.ForeignKey(
        'animals.Animal', 
        on_delete=models.SET_NULL, 
        related_name='products',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.description} ({self.product_type.name})"


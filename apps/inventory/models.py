from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Inventory(models.Model):
    # The Specific Item (e.g., the specific Resource "Booster" or Product "Milk")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    
    # Hierarchical Details
    category_name = models.CharField(max_length=100) # e.g., "Vaccine", "Feed", "Cattle"
    item_name = models.CharField(max_length=255)     # e.g., "Booster", "Grass", "Cow-01"
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit = models.CharField(
        max_length=50, 
        choices=[("Liters", "Liters"), ("KGs", "KGs"), ("Units", "Units")]
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate entries for the same specific item
        unique_together = ('content_type', 'object_id')

    def __str__(self):
        return f"[{self.category_name}] {self.item_name} - {self.quantity} {self.unit}"
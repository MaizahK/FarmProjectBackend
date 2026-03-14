from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Inventory(models.Model):
    # Link to the Type of content (e.g., Animal Model, Resource Model)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # We remove object_id from uniqueness to allow grouping
    category_name = models.CharField(max_length=100) # e.g., "Cow", "Feed", "Vaccine"
    item_name = models.CharField(max_length=255)     # e.g., "Angus", "Corn Sacks", "Booster"
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit = models.CharField(
        max_length=50, 
        choices=[("Liters", "Liters"), ("KGs", "KGs"), ("Units", "Units")]
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Now unique based on the NAME and CATEGORY, not the specific ID
        unique_together = ('content_type', 'category_name', 'item_name')

    def __str__(self):
        return f"[{self.category_name}] {self.item_name} - {self.quantity} {self.unit}"
class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('PRODUCTION', 'Production'),
        ('CONSUMPTION', 'Consumption'),
        ('PURCHASE', 'Purchase'),
        ('SALE', 'Sale'),
        ('ADJUSTMENT', 'Adjustment'),
        ('TRANSFER', 'Transfer'),
    ]

    # The Item being moved (Animal, Resource, Product)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="inventory_items")
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    # Where this transaction came from (e.g., a specific Sale ID or Production ID)
    reference_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, related_name="transaction_references")
    reference_id = models.PositiveIntegerField(null=True, blank=True)
    reference_object = GenericForeignKey('reference_type', 'reference_id')

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.quantity} for {self.object_id}"
from django.db import models
from apps.animals.models import Animal # Assuming your app is structured this way

class AdalRecord(models.Model):
    animal = models.ForeignKey(
        Animal, 
        on_delete=models.CASCADE, 
        related_name='adal_records'
    )
    price_before = models.DecimalField(max_digits=12, decimal_places=2)
    price_after = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    date_sent = models.DateField()
    date_received = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adal: {self.animal.tag_id} ({self.date_sent})"
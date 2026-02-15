from django.db import models
from resources.models import Resource

class VaccinationRecord(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='vaccinations')
    # Link to Resource with type restricted (logic handled in validation or UI)
    vaccine_resource = models.ForeignKey(Resource, on_delete=models.PROTECT) 
    
    date_administered = models.DateField()
    administered_by = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50)
    next_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vaccine_resource.name} -> {self.animal.tag_id}"
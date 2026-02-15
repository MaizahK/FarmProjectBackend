# Create your models here.
from django.db import models

class Animal(models.Model):
    SPECIES_CHOICES = [('Bovine', 'Bovine'), ('Equine', 'Equine'), ('Porcine', 'Porcine')]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    tag_id = models.CharField(max_length=50, unique=True) # Ear tag
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    health_status = models.CharField(max_length=100, default="Healthy")
    last_vaccination = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True) # For sold/deceased tracking

    def __str__(self):
        return f"{self.tag_id} - {self.species}"
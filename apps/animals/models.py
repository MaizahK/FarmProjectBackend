from django.conf import settings
from django.db import models

class AnimalPurpose(models.Model):
    SPECIES_CHOICES = [
        ('Cow', 'Cow'),
        ('Sheep', 'Sheep'),
        ('Goat', 'Goat'),
        ('Chicken', 'Chicken')
    ]
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.species} - {self.name}"

class Animal(models.Model):
    SPECIES_CHOICES = [('Cow', 'Cow'), ('Sheep', 'Sheep'), ('Goat', 'Goat'), ('Chicken', 'Chicken')]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    HEALTH_CHOICES = [('healthy', 'Healthy'), ('ill', 'Ill/In Treatment'), ('quarantine', 'Quarantine')]
    
    # Added Status Choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('died', 'Died'),
        ('transferred', 'Transferred'),
    ]

    tag_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='animals', null=True, blank=True)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    notes = models.CharField(max_length=5000, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='healthy')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='animals', null=True, blank=True)
    purpose = models.ForeignKey(AnimalPurpose, on_delete=models.SET_NULL, null=True, blank=True, related_name='animals')
    
    last_vet_check = models.DateTimeField(null=True, blank=True)
    dam = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="offspring_from_dam", limit_choices_to={'gender': 'F'})
    sire = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="offspring_from_sire", limit_choices_to={'gender': 'M'})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tag_id} - {self.species}"

class AnimalHistory(models.Model):
    TYPE_CHOICES = [
        ('Vaccination', 'Vaccination'),
        ('Health Checkup', 'Health Checkup'),
        ('Treatment', 'Treatment'),
        ('Other', 'Other'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='history')
    event_name = models.CharField(max_length=255) # e.g., "FMD Vaccine"
    record_type = models.CharField(max_length=50
                                #    choices=TYPE_CHOICES
                                   )
    description = models.TextField(blank=True)
    event_date = models.DateField(auto_now_add=True)
    performed_by = models.CharField(max_length=100, blank=True)
    next_due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.record_type}: {self.event_name} - {self.animal.tag_id}"
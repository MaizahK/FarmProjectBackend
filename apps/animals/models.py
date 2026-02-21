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

    def __str__(self):
        return f"{self.species} - {self.name}"


class Animal(models.Model):
    SPECIES_CHOICES = [
        ('Cow', 'Cow'),
        ('Sheep', 'Sheep'),
        ('Goat', 'Goat'),
        ('Chicken', 'Chicken')
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    HEALTH_CHOICES = [
        ('healthy', 'Healthy'),
        ('ill', 'Ill/In Treatment'),
        ('quarantine', 'Quarantine'),
    ]

    tag_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    notes = models.CharField(max_length=5000, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES,
        default='healthy'
    )
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='animals',
        null=True,
        blank=True
    )

    last_vet_check = models.DateTimeField(null=True, blank=True)

    # ✅ Purpose Field
    purpose = models.ForeignKey(
        AnimalPurpose,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='animals'
    )

    # ✅ Self-referencing fields
    dam = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offspring_from_dam",
        limit_choices_to={'gender': 'F'}
    )

    sire = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offspring_from_sire",
        limit_choices_to={'gender': 'M'}
    )

    def __str__(self):
        return f"{self.tag_id} - {self.species}"


class VaccinationRecord(models.Model):
    animal = models.ForeignKey(
        'Animal',
        on_delete=models.CASCADE,
        related_name='vaccinations'
    )

    # Link to Resource with type restricted (validation handled elsewhere)
    vaccine_resource = models.ForeignKey(
        'resources.Resource',
        on_delete=models.PROTECT
    )

    date_administered = models.DateField()
    administered_by = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50)
    next_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vaccine_resource.name} -> {self.animal.tag_id}"
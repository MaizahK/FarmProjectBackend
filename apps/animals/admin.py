from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Animal)
admin.site.register(VaccinationRecord)
admin.site.register(AnimalPurpose)
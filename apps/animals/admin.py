from django.contrib import admin
from .models.animals import *
from .models.vaccination_records import *

# Register your models here.
admin.site.register(Animal)
admin.site.register(VaccinationRecord)
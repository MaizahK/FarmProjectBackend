# project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'vaccination-records', VaccinationRecordViewSet)
router.register(r'health-records', HealthRecordViewSet)
router.register(r'animal-purposes', AnimalPurposeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # ... your JWT auth paths
]
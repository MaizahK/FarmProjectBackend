# project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, VaccinationRecordViewSet

router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'vaccinations', VaccinationRecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # ... your JWT auth paths
]
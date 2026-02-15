from django.urls import path
from .views import AnimalGateWayView

urlpatterns = [
    path('', AnimalGateWayView.as_view(), name='animals'),
]

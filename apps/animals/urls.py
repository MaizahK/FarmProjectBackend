from django.urls import path
from .views import AnimalViewSet

urlpatterns = [
    path('list/', AnimalViewSet.as_view({'get': 'list'}), name='animal-list'),
    path('<int:pk>/', AnimalViewSet.as_view({'get': 'retrieve'}), name='animal-detail'),
]

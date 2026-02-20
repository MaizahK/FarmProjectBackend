from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, ResourceTypeViewSet

router = DefaultRouter()
router.register(r'resource-types', ResourceTypeViewSet)
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
# project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'assign-permissions', AssignPermissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
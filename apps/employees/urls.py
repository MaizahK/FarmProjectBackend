from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeTypeViewSet

router = DefaultRouter()
router.register(r'employee-types', EmployeeTypeViewSet, basename='employee-types')
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('api/', include(router.urls)),
]
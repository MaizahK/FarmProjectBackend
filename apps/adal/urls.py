# project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'adal-records', AdalRecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
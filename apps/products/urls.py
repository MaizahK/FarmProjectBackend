from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'product-types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
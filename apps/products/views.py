from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductType
from .serializers import ProductSerializer, ProductTypeSerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optional: Filter Products by type via URL query params
        Example: /api/Products/?type=Vaccine
        """
        queryset = Product.objects.all()
        rt_name = self.request.query_params.get('type')
        if rt_name:
            queryset = queryset.filter(Product_type__name__iexact=rt_name)
        return queryset
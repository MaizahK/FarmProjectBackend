from rest_framework import serializers
from .models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # This makes the API response more readable
    product_type_name = serializers.ReadOnlyField(source='product_type.name')

    class Meta:
        model = Product
        fields = ['id', 'product_type', 'product_type_name', 'description', 'quantity']
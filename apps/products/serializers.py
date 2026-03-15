from rest_framework import serializers
from .models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    product_type_name = serializers.ReadOnlyField(source='product_type.name')
    # Transient field for inventory logic
    add_to_inventory = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Product
        fields = [
            'id', 'product_type', 'product_type_name', 'description', 
            'quantity', 'unit', 'animal', 'add_to_inventory', 'is_deleted'
        ]

    def create(self, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().update(instance, validated_data)
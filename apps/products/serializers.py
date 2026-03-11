from rest_framework import serializers
from .models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # This makes the API response more readable
    product_type_name = serializers.ReadOnlyField(source='product_type.name')
    add_in_inventory = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Product
        fields = ['id', 'product_type', 'product_type_name', 'description', 'quantity', 'unit', 'add_in_inventory', 'is_deleted']


    def create(self, validated_data):
        # Ensure transient `add_in_inventory` is not passed into the model create()
        self._add_in_inventory = validated_data.pop('add_in_inventory', False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure transient `add_in_inventory` is not passed into the model update()
        self._add_in_inventory = validated_data.pop('add_in_inventory', False)
        return super().update(instance, validated_data)

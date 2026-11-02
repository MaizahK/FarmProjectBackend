from rest_framework import serializers
from .models import Product, ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description',  'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    product_type_name = serializers.ReadOnlyField(source='product_type.name')
    # Transient field for inventory logic
    add_to_inventory = serializers.BooleanField(write_only=True, required=False, default=False)
    # Day the batch was produced, for batches entered after the fact (default: now).
    # Stored in created_at, which the app already treats as the batch date.
    date = serializers.DateField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_type', 'product_type_name', 'description',
            'quantity', 'unit', 'animal', 'add_to_inventory', 'is_deleted',  'created_at', 'updated_at',
            'date'
        ]

    def create(self, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        validated_data.pop('date', None)  # applied by ProductViewSet.perform_create
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        validated_data.pop('date', None)
        return super().update(instance, validated_data)
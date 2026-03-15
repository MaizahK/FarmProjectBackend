from rest_framework import serializers
from .models import Resource, ResourceType

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['id', 'name', 'description']

class ResourceSerializer(serializers.ModelSerializer):
    resource_type_name = serializers.ReadOnlyField(source='resource_type.name')
    # Transient fields for logic processing
    add_to_inventory = serializers.BooleanField(write_only=True, required=False, default=False)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, write_only=True, required=False)

    class Meta:
        model = Resource
        fields = [
            'id', 'resource_type', 'resource_type_name', 'name', 
            'vendor', 'quantity', 'unit', 'add_to_inventory', 
            'amount', 'is_deleted'
        ]

    def create(self, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        self._amount = validated_data.pop('amount', 0)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        self._amount = validated_data.pop('amount', 0)
        return super().update(instance, validated_data)
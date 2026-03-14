from rest_framework import serializers
from .models import Resource, ResourceType

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['id', 'name', 'description']

class ResourceSerializer(serializers.ModelSerializer):
    # This makes the API response more readable
    resource_type_name = serializers.ReadOnlyField(source='resource_type.name')
    add_to_inventory = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Resource
        fields = ['id', 'resource_type', 'resource_type_name', 'name', 'vendor', 'quantity', 'unit', 'add_to_inventory', 'is_deleted']


    def create(self, validated_data):
        # Ensure transient `add_to_inventory` is not passed into the model create()
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure transient `add_to_inventory` is not passed into the model update()
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().update(instance, validated_data)

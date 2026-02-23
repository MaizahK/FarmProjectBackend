from rest_framework import serializers
from .models import Resource, ResourceType

class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ['id', 'name', 'description']

class ResourceSerializer(serializers.ModelSerializer):
    # This makes the API response more readable
    resource_type_name = serializers.ReadOnlyField(source='resource_type.name')

    class Meta:
        model = Resource
        fields = ['id', 'resource_type', 'resource_type_name', 'name', 'vendor', 'quantity']
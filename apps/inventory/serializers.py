from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Inventory, InventoryTransaction

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryTransactionSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    reference_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'content_type', 'object_id', 'reference_type', 'reference_id',
            'transaction_type', 'quantity', 'description', 'notes', 'created_at'
        ]
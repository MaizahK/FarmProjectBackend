from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Inventory, InventoryTransaction

class InventorySerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
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
    category_name = serializers.CharField(write_only=True)
    item_name = serializers.CharField(write_only=True)

    class Meta:
        model = InventoryTransaction
        fields = '__all__'


    def create(self, validated_data):
        # Pop the extra values so they don't cause a database error
        self._category_name = validated_data.pop('category_name', 'General')
        self._item_name = validated_data.pop('item_name', 'Unknown')
        
        return super().create(validated_data)
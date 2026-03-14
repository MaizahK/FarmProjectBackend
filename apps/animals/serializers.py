from rest_framework import serializers
from django.utils import timezone
from .models import Animal, AnimalPurpose, AnimalHistory

class AnimalPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalPurpose
        fields = ['id', 'name', 'species']

class AnimalHistorySerializer(serializers.ModelSerializer):
    animal_tag = serializers.ReadOnlyField(source='animal.tag_id')

    class Meta:
        model = AnimalHistory
        fields = [
            'id', 'animal', 'animal_tag', 'event_name', 'record_type', 
            'description', 'event_date', 'performed_by', 'next_due_date'
        ]

class AnimalSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    purpose_name = serializers.ReadOnlyField(source='purpose.name')
    age = serializers.SerializerMethodField()
    history = AnimalHistorySerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    add_to_inventory = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Animal
        fields = [
            'id', 'tag_id', 'name', 'species', 'breed', 'gender', 
            'birth_date', 'weight', 'health_status', 'status', 'owner', 
            'owner_name', 'purpose', 'purpose_name', 'age', 
            'last_vet_check', 'notes', 'image', 'history', 
            'add_to_inventory', 'is_active', 'is_deleted'
        ]
        read_only_fields = ['owner']

    def get_age(self, obj):
        if obj.birth_date:
            delta = timezone.now().date() - obj.birth_date
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} years, {months} months"
        return "Unknown"

    def create(self, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_to_inventory = validated_data.pop('add_to_inventory', False)
        return super().update(instance, validated_data)
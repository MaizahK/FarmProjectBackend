from rest_framework import serializers
from django.utils import timezone
from .models import *

class AnimalPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalPurpose
        fields = ['id', 'name', 'species']

class VaccinationRecordSerializer(serializers.ModelSerializer):
    animal_tag = serializers.ReadOnlyField(source='animal.tag_id')
    vaccine_name = serializers.ReadOnlyField(source='vaccine_resource.name')

    class Meta:
        model = VaccinationRecord
        fields = [
            'id', 'animal', 'animal_tag', 'vaccine_resource', 
            'vaccine_name', 'date_administered', 'administered_by', 
            'batch_number', 'next_due_date'
        ]

class HealthRecordSerializer(serializers.ModelSerializer):
    # Pulling the tag_id from the related Animal model for display
    animal_tag = serializers.ReadOnlyField(source='animal.tag_id')

    class Meta:
        model = HealthRecord
        fields = [
            'id', 
            'animal', 
            'animal_tag', 
            'date_checkup', 
            'description', 
            'checked_by', 
            'next_due_date'
        ]

class AnimalSerializer(serializers.ModelSerializer):
    # Read-only fields for the API response
    owner_name = serializers.ReadOnlyField(source='owner.username')
    purpose_name = serializers.ReadOnlyField(source='purpose.name')
    age = serializers.SerializerMethodField()
    vaccination_records = VaccinationRecordSerializer(many=True, read_only=True)
    health_records = HealthRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = [
            'id', 'tag_id', 'name', 'species', 'breed', 
            'gender', 'birth_date', 'weight', 'health_status', 
            'owner', 'owner_name', 'purpose', 'purpose_name', 
            'age', 'last_vet_check', 'notes',
            'vaccination_records', 'health_records'
        ]
        read_only_fields = ['owner']

    def get_age(self, obj):
        """Calculates age in months or years based on birth_date."""
        if obj.birth_date:
            delta = timezone.now().date() - obj.birth_date
            years = delta.days // 365
            months = (delta.days % 365) // 30
            return f"{years} years, {months} months"
        return "Unknown"
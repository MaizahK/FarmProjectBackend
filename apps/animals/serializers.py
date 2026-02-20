# api/serializers.py
from rest_framework import serializers
from .models.animals import Animal
from .models.vaccination_records import VaccinationRecord

class AnimalSerializer(serializers.ModelSerializer):
    # Read-only fields for the API response
    owner_name = serializers.ReadOnlyField(source='owner.username')
    age = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = [
            'id', 'tag_id', 'name', 'species', 'breed', 
            'gender', 'birth_date', 'weight', 'health_status', 
            'owner', 'owner_name', 'age', 'last_vet_check'
        ]
        read_only_fields = ['owner']

    def get_age(self, obj):
        """Calculates age in months or years based on birth_date."""
        from django.utils import timezone
        if obj.birth_date:
            delta = timezone.now().date() - obj.birth_date
            return f"{delta.days // 365} years, {(delta.days % 365) // 30} months"
        return "Unknown"
    
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
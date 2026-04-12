from rest_framework import serializers
from .models import AdalRecord

class AdalRecordSerializer(serializers.ModelSerializer):
    animal_tag = serializers.ReadOnlyField(source='animal.tag_id')
    animal_species = serializers.ReadOnlyField(source='animal.species')

    class Meta:
        model = AdalRecord
        fields = [
            'id', 'animal', 'animal_tag', 'animal_species', 
            'price_before', 'price_after', 
            'date_sent', 'date_received', 'notes', 'created_at'
        ]
from rest_framework import serializers

class AnimalAssetSerializer(serializers.Serializer):
    # Attributes
    id = serializers.UUIDField(required=False, read_only=True)
    name = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=['active', 'archived'], default='active')
    birthdate = serializers.DateTimeField(required=False, allow_null=True)
    sex = serializers.ChoiceField(choices=[('F', 'Female'), ('M', 'Male')], required=False)
    is_castrated = serializers.BooleanField(default=False)
    nickname = serializers.ListField(child=serializers.CharField(), required=False)
    notes = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        attributes = instance.get('attributes', {})

        notes = attributes.get('notes')

        return {
            'id': instance.get('id'),
            'name': attributes.get('name'),
            'status': attributes.get('status'),
            'birthdate': attributes.get('birthdate'),
            'sex': attributes.get('sex'),
            'is_castrated': attributes.get('is_castrated'),
            'nickname': attributes.get('nickname', []),
            'notes': notes.get('value', '') if isinstance(notes, dict) else '',
        }


    def to_internal_value(self, data):
        """Wrap flat user data into the farmOS JSON:API structure for sending."""
        validated_data = super().to_internal_value(data)
        
        farmos_payload = {
            "data": {
                "type": "asset--animal",
                "attributes": {
                    "name": validated_data.get('name'),
                    "status": validated_data.get('status'),
                    "birthdate": validated_data.get('birthdate'),
                    "sex": validated_data.get('sex'),
                    "is_castrated": validated_data.get('is_castrated'),
                    "nickname": validated_data.get('nickname', []),
                    "notes": {
                        "value": validated_data.get('notes', ''),
                        "format": "plain_text"
                    }
                }
            }
        }
        return farmos_payload
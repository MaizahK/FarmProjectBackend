from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    # We use a SlugRelatedField or nested serializer for reading, 
    # but a PrimaryKeyRelatedField for writing.
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 
            'last_name', 'phone_number', 'role', 'role_name', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Ensure password hashing
        user = User.objects.create_user(**validated_data)
        return user
from rest_framework import serializers
from .models import *

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

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']
        
class BulkPermissionSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(help_text="ID of the role")
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        required=False, 
        help_text="List of permission IDs"
    )
    all_perms = serializers.BooleanField(
        required=False, 
        default=False, 
        help_text="If true, ignores permission_ids and targets all available permissions"
    )
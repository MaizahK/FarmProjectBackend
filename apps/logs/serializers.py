from rest_framework import serializers
# Make sure to import ActivityLog from your local models
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'title', 'description', 'module', 'username', 'created_at']
        read_only_fields = ['username', 'created_at']
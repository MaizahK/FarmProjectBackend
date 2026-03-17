from rest_framework import serializers
from .models import Employee, EmployeeType

class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    is_recurring = serializers.BooleanField(write_only=True, default=False)
    # Using the ID for creation, but we could also use a nested serializer for GET
    employee_type_name = serializers.ReadOnlyField(source='employee_type.name')

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_type', 'employee_type_name', 'first_name', 
            'last_name', 'email', 'salary', 'position', 'hire_date', 'is_recurring'
        ]
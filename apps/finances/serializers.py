from rest_framework import serializers
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class RecurringExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpenseType
        fields = '__all__'

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = '__all__'
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense, FinancialTransaction

class FinancialTransactionSerializer(serializers.ModelSerializer):
    # Transient Fields
    ref_model = serializers.CharField(write_only=True)
    item_id = serializers.IntegerField(write_only=True, required=False, default=0)
    qty = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=False, default=0)
    unit = serializers.CharField(write_only=True, required=False, default="Units")
    is_recurring = serializers.BooleanField(write_only=True, default=False)
    recurring_type = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    is_standalone = serializers.BooleanField(write_only=True, default=False)
    is_paid = serializers.BooleanField(write_only=True, default=True)

    class Meta:
        model = FinancialTransaction
        fields = [
            'id', 'type', 'amount', 'category', 'item_name', 'ref_model', 'item_id', 
            'qty', 'unit', 'payment_method', 'notes', 'created_at',
            'is_recurring', 'recurring_type', 'is_standalone', 'is_paid'
        ]

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['total_amount']

class RecurringExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpenseType
        fields = '__all__'

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = '__all__'
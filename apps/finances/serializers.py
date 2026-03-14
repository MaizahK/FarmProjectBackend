from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense, FinancialTransaction

class FinancialTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialTransaction
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all())
    
    class Meta:
        model = Sale
        fields = ['id', 'content_type', 'object_id', 'quantity', 'price_per_item', 'total_amount', 'sale_date', 'notes']
        read_only_fields = ['total_amount']

class ExpenseSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(slug_field='model', queryset=ContentType.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Expense
        fields = ['id', 'content_type', 'object_id', 'category_name', 'amount', 'is_paid', 'expense_date', 'description']

class RecurringExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpenseType
        fields = '__all__'

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = '__all__'
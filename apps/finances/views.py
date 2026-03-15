from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.contrib.contenttypes.models import ContentType
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense, FinancialTransaction
from .serializers import (
    SaleSerializer, ExpenseSerializer, FinancialTransactionSerializer,
    RecurringExpenseTypeSerializer, RecurringExpenseSerializer
)
from .utils import process_financial_flow

class FinancialTransactionViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        ref_data = {
            'object_id': data.get('item_id', 0),
            'quantity': data.get('qty', 0),
            'unit': data.get('unit', 'Units'),
            'notes': data.get('notes', ''),
            'is_paid': data.get('is_paid', True),
            'description': data.get('notes', f"Transaction for {data['category']}")
        }

        try:
            process_financial_flow(
                user=request.user,
                tx_type=data['type'],
                amount=data['amount'],
                category=data['category'],
                item_name=data['item_name'],
                ref_model=data['ref_model'],
                ref_data=ref_data,
                is_standalone=data.get('is_standalone', False),
                is_recurring=data.get('is_recurring', False),
                recurring_type_id=data.get('recurring_type')
            )
            return Response({"status": "Transaction successfully recorded"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def perform_create(self, serializer):
        with db_transaction.atomic():
            sale = serializer.save()

            # Create the Ledger entry automatically
            FinancialTransaction.objects.create(
                type='INCOME',
                amount=sale.total_amount,
                category=sale.category_name,
                reference_type=ContentType.objects.get_for_model(sale),
                reference_id=sale.id,
                notes=sale.notes
            )

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        with db_transaction.atomic():
            expense = serializer.save()
            
            is_recurring = serializer.validated_data.get('is_recurring', False)
            recurring_type_id = serializer.validated_data.get('recurring_type')

            if is_recurring and recurring_type_id:
                r_type = RecurringExpenseType.objects.get(id=recurring_type_id)
                RecurringExpense.objects.get_or_create(
                    expense_type=r_type,
                    name=expense.category_name,
                    user=self.request.user,
                    defaults={'amount': expense.amount}
                )

            # Create the Ledger entry automatically
            FinancialTransaction.objects.create(
                type='EXPENSE',
                amount=expense.amount,
                category=expense.category_name,
                reference_type=ContentType.objects.get_for_model(expense),
                reference_id=expense.id,
                notes=expense.description
            )

class RecurringExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpenseType.objects.all()
    serializer_class = RecurringExpenseTypeSerializer

class RecurringExpenseViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
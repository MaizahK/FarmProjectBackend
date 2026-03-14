from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense, FinancialTransaction
from .serializers import *
from .utils import process_full_sale, record_expense_flow

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def perform_create(self, serializer):
        sale = serializer.save()
        process_full_sale(self.request.user, sale)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        expense = serializer.save()
        record_expense_flow(self.request.user, expense)

class FinancialTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer

class RecurringExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpenseType.objects.all()
    serializer_class = RecurringExpenseTypeSerializer

class RecurringExpenseViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
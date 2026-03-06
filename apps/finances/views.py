from rest_framework import viewsets
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense
from .serializers import (
    SaleSerializer, ExpenseSerializer, 
    RecurringExpenseTypeSerializer, RecurringExpenseSerializer
)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class RecurringExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpenseType.objects.all()
    serializer_class = RecurringExpenseTypeSerializer

class RecurringExpenseViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
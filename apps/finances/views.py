from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.contrib.contenttypes.models import ContentType
from .models import Sale, Expense, RecurringExpenseType, RecurringExpense, FinancialTransaction
from .serializers import *
from .utils import process_unified_transaction, reverse_financial_record

class FinancialTransactionViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            process_unified_transaction(
                user=request.user,
                tx_type=serializer.validated_data['type'],
                amount=serializer.validated_data['amount'],
                category=serializer.validated_data['category'],
                item_name=serializer.validated_data['item_name'],
                ref_model=serializer.validated_data['ref_model'],
                data=serializer.validated_data
            )
            return Response({"status": "Success"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # str(e) would render as "[ErrorDetail(string=...)]" in the app
            message = e.detail[0] if isinstance(e.detail, list) else e.detail
            return Response({"error": str(message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def perform_create(self, serializer):
        with db_transaction.atomic():
            sale = serializer.save()
            FinancialTransaction.objects.create(
                type='INCOME', amount=sale.total_amount, category=sale.category_name,
                item_name=sale.category_name, reference_type=ContentType.objects.get_for_model(sale),
                reference_id=sale.id
            )
            # Logger.write(...) call here if needed

    def perform_update(self, serializer):
        instance = self.get_object()
        old_total = instance.total_amount

        with db_transaction.atomic():
            # Stock was moved when the sale was created, so the sold item and
            # quantity stay fixed; only price, paid status and notes change.
            sale = serializer.save(
                content_type=instance.content_type,
                object_id=instance.object_id,
                category_name=instance.category_name,
                quantity=instance.quantity,
            )

            # Same audit-trail approach as expense edits
            if old_total != sale.total_amount:
                FinancialTransaction.objects.create(
                    type='INCOME',
                    amount=sale.total_amount,
                    category=sale.category_name,
                    item_name=sale.category_name,
                    reference_type=ContentType.objects.get_for_model(sale),
                    reference_id=sale.id,
                    notes=f"Amount updated from {old_total:.2f} to {sale.total_amount:.2f}"
                )

    def perform_destroy(self, instance):
        # Voiding a sale returns its stock and removes its ledger rows
        with db_transaction.atomic():
            reverse_financial_record(self.request.user, instance)
            instance.delete()

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        with db_transaction.atomic():
            expense = serializer.save()
            FinancialTransaction.objects.create(
                type='EXPENSE', amount=expense.amount, category=expense.category_name,
                item_name=expense.category_name, reference_type=ContentType.objects.get_for_model(expense),
                reference_id=expense.id
            )
    
    def perform_update(self, serializer):
        # 1. Get the current state from the DB before saving
        instance = self.get_object()
        old_amount = instance.amount
        old_category = instance.category_name

        with db_transaction.atomic():
            # 2. Save the new changes
            expense = serializer.save()
            
            # 3. Detect changes and create a Ledger entry for the audit trail
            changes = []
            if old_amount != expense.amount:
                changes.append(f"Amount updated from {old_amount} to {expense.amount}")
            
            if old_category != expense.category_name:
                changes.append(f"Category updated from '{old_category}' to '{expense.category_name}'")

            # 4. Only create a transaction entry if something actually changed
            if changes:
                FinancialTransaction.objects.create(
                    type='EXPENSE', 
                    amount=expense.amount, 
                    category=expense.category_name,
                    item_name=expense.category_name, 
                    reference_type=ContentType.objects.get_for_model(expense),
                    reference_id=expense.id,
                    notes=" | ".join(changes) # Combines multiple changes into one note
                )

    def perform_destroy(self, instance):
        # Deleting a purchase takes its stock back out and removes its ledger rows
        with db_transaction.atomic():
            reverse_financial_record(self.request.user, instance)
            instance.delete()

class RecurringExpenseTypeViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpenseType.objects.all()
    serializer_class = RecurringExpenseTypeSerializer

    def destroy(self, request, *args, **kwargs):
        # The FK cascades, so deleting a used type would silently delete its recurring expenses
        in_use = RecurringExpense.objects.filter(expense_type=self.get_object()).count()
        if in_use:
            return Response(
                {"error": f"This type is used by {in_use} recurring expense(s). Delete or change those first."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

class RecurringExpenseViewSet(viewsets.ModelViewSet):
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
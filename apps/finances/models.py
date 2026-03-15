from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class FinancialTransaction(models.Model):
    TRANSACTION_TYPES = [('INCOME', 'Income'), ('EXPENSE', 'Expense')]
    
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    
    reference_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    reference_id = models.PositiveIntegerField()
    reference_object = GenericForeignKey('reference_type', 'reference_id')
    
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.amount} ({self.category})"

class Sale(models.Model):
    # Link to the item being sold
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    # --- Fields Added to Match Expense Model ---
    category_name = models.CharField(max_length=100, help_text="e.g., Poultry Sales")
    is_paid = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    # -------------------------------------------

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price_per_item
        super().save(*args, **kwargs)

class Expense(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')

    category_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    expense_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

class RecurringExpenseType(models.Model):
    name = models.CharField(max_length=100)

class RecurringExpense(models.Model):
    expense_type = models.ForeignKey(RecurringExpenseType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
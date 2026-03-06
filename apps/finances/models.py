from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Sale(models.Model):
    # Link to Inventory or any other model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Sale: {self.item} - {self.total_amount}"

class Expense(models.Model):
    # Link to Inventory (for buying feed) or other models
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('content_type', 'object_id')

    category_name = models.CharField(max_length=100) # e.g., "Utility", "Salary", "Feed"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    expense_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Expense: {self.description} - {self.amount}"

class RecurringExpenseType(models.Model):
    name = models.CharField(max_length=100) # e.g., "Utility Bill", "Salary"

    def __str__(self):
        return self.name

class RecurringExpense(models.Model):
    expense_type = models.ForeignKey(RecurringExpenseType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # e.g., "Electricity Bill" or "Staff A Salary"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.expense_type.name})"
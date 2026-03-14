from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FinancialTransaction)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(RecurringExpenseType)
admin.site.register(RecurringExpense)

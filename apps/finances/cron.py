from django_cron import CronJobBase, Schedule
from .models import RecurringExpense, Expense

class MonthlyRecurringExpenseCronJob(CronJobBase):
    RUN_EVERY_MINS = 43200 # Roughly once a month (30 days)
    # Alternatively, use a custom schedule if your library supports crontab syntax

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'finances.monthly_recurring_expense_cron' 

    def do(self):
        recurring_items = RecurringExpense.objects.all()
        for item in recurring_items:
            Expense.objects.create(
                category_name=item.expense_type.name,
                amount=item.amount,
                description=f"Monthly Recurring: {item.name}",
                is_paid=False # Usually starts as unpaid until processed
            )
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from .models import RecurringExpense, Expense

class MonthlyRecurringExpenseCronJob(CronJobBase):
    RUN_EVERY_MINS = 43200 # Roughly once a month (30 days)
    # Alternatively, use a custom schedule if your library supports crontab syntax

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'finances.monthly_recurring_expense_cron' 

    def do(self):
        # Range filter rather than __month: MySQL may lack timezone tables
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        recurring_items = RecurringExpense.objects.all()
        for item in recurring_items:
            description = f"Monthly Recurring: {item.name}"
            # Skip if this month's entry already exists (e.g. job ran twice)
            if Expense.objects.filter(description=description, expense_date__gte=month_start).exists():
                continue
            Expense.objects.create(
                category_name=item.expense_type.name,
                amount=item.amount,
                description=description,
                is_paid=False # Usually starts as unpaid until processed
            )
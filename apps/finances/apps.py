from django.apps import AppConfig


# Cron jobs are run by the system crontab (`manage.py runcrons`), not from here:
# a thread in ready() would start once per gunicorn worker and run jobs in parallel.
class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.finances"
from django.apps import AppConfig
import threading
import time
from django.core.management import call_command


class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.finances"

    def ready(self):
        def run_cron():
            while True:
                call_command("runcrons")
                time.sleep(60)

        threading.Thread(target=run_cron, daemon=True).start()
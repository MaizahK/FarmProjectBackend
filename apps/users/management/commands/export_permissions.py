import csv
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin


class Command(BaseCommand):
    help = "Export DRF endpoints to CSV for Permission table"

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        url_patterns = resolver.url_patterns

        endpoints = []

        def extract(patterns, prefix=""):
            for pattern in patterns:
                if hasattr(pattern, "url_patterns"):
                    extract(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    path = prefix + str(pattern.pattern)

                    # Remove admin endpoints
                    if "admin" in path:
                        continue

                    callback = pattern.callback
                    view = getattr(callback, "cls", None)

                    if not view:
                        continue

                    methods = []

                    if issubclass(view, APIView):
                        methods = [
                            m.upper()
                            for m in view.http_method_names
                            if hasattr(view, m)
                        ]

                    if issubclass(view, ViewSetMixin):
                        if hasattr(callback, "actions"):
                            methods = [m.upper() for m in callback.actions.keys()]

                    for method in methods:
                        endpoints.append({
                            "name": f"{method} /{path}",
                            "path": f"/{path}",
                            "method": method
                        })

        extract(url_patterns)

        # Remove duplicates
        endpoints = {
            (e["path"], e["method"]): e for e in endpoints
        }.values()

        with open("permissions.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["id", "name", "path", "method"])

            for idx, ep in enumerate(endpoints, start=1):
                writer.writerow([
                    idx,
                    ep["name"],
                    ep["path"],
                    ep["method"]
                ])

        self.stdout.write(self.style.SUCCESS("permissions.csv generated successfully"))

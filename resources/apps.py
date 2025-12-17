# resources/apps.py
from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resources"

    def ready(self):
        """
        Seed default Subject rows, but *only* when the DB is ready.

        We wrap everything in a try/except so that:
        - makemigrations/migrate won't crash if the table/columns don't exist yet.
        """
        from django.db.utils import OperationalError, ProgrammingError
        from django.db import connections
        from .models import Subject

        default_subjects = [
            "C Programming",
            "Python",
            "Data Structures",
            "DBMS",
            "Computer Networks",
            "Operating Systems",
            "Compiler Design",
            "Artificial Intelligence",
        ]

        try:
            # Make sure the table itself exists before querying
            conn = connections["default"]
            tables = conn.introspection.table_names()
            if Subject._meta.db_table not in tables:
                return  # subject table not created yet → skip

            for sub in default_subjects:
                Subject.objects.get_or_create(name=sub)

        except (OperationalError, ProgrammingError):
            # Database schema not ready (e.g., missing column like 'branch')
            # → silently skip seeding during startup.
            return

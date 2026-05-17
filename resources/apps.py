# resources/apps.py
from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resources"

    def ready(self):
        """
        Seed default Subject rows on startup.
        Uses (name, abbreviation) as the seed definition.
        Skips gracefully if the DB table or columns aren't ready yet.
        """
        from django.db.utils import OperationalError, ProgrammingError
        from django.db import connections
        from .models import Subject

        # (full_name, abbreviation, branch)
        DEFAULT_SUBJECTS = [
            ("C Programming",                        "C",     ""),
            ("Python Programming",                   "Python",""),
            ("Java Programming",                     "Java",  ""),
            ("Data Structures",                      "DS",    ""),
            ("Design and Analysis of Algorithms",    "DAA",   ""),
            ("Database Management System",           "DBMS",  ""),
            ("Computer Networks",                    "CN",    ""),
            ("Operating System",                     "OS",    ""),
            ("Compiler Design",                      "CD",    ""),
            ("Formal Languages and Automata Theory", "FLAT",  ""),
            ("Artificial Intelligence",              "AI",    ""),
            ("Machine Learning",                     "ML",    ""),
            ("Software Engineering",                 "SE",    ""),
            ("Computer Organization",                "CO",    ""),
            ("Digital Logic Design",                 "DLD",   ""),
            ("Others / General",                     "",      ""),
        ]

        try:
            conn = connections["default"]
            tables = conn.introspection.table_names()
            if Subject._meta.db_table not in tables:
                return  # table not yet created → skip

            for name, abbrev, branch in DEFAULT_SUBJECTS:
                # Try get by name first, then by abbreviation to avoid duplicates
                existing = Subject.objects.filter(name=name)
                if existing.count() == 0:
                    # Also check if there's a record with the abbreviation as the name
                    if abbrev:
                        old = Subject.objects.filter(name=abbrev)
                        if old.count() == 1:
                            # Upgrade the old abbreviation-named record
                            s = old.first()
                            s.name = name
                            s.abbreviation = abbrev
                            if branch:
                                s.branch = branch
                            s.save()
                            continue
                        elif old.count() > 1:
                            # Keep first, delete the rest
                            first = old.first()
                            old.exclude(pk=first.pk).delete()
                            first.name = name
                            first.abbreviation = abbrev
                            first.save()
                            continue
                    Subject.objects.create(name=name, abbreviation=abbrev, branch=branch)
                elif existing.count() == 1:
                    # Update abbreviation if blank
                    s = existing.first()
                    changed = False
                    if not s.abbreviation and abbrev:
                        s.abbreviation = abbrev
                        changed = True
                    if changed:
                        s.save(update_fields=["abbreviation"])
                else:
                    # Duplicates: keep first, delete rest
                    first = existing.first()
                    existing.exclude(pk=first.pk).delete()
                    if not first.abbreviation and abbrev:
                        first.abbreviation = abbrev
                        first.save(update_fields=["abbreviation"])

        except (OperationalError, ProgrammingError):
            return

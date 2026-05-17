"""
Management command: auto-fill Subject abbreviations for common CS/ECE subjects.
Run: python manage.py populate_subject_abbreviations

Only fills abbreviation if it is currently blank — never overwrites existing values.
"""
from django.core.management.base import BaseCommand
from resources.models import Subject


# Map of subject name keywords → abbreviation
# The key is a lowercase substring to match in the subject name.
KNOWN_ABBREVS = {
    "operating system": "OS",
    "data structure": "DS",
    "database management": "DBMS",
    "database system": "DBMS",
    "computer network": "CN",
    "computer organization": "CO",
    "computer architecture": "CA",
    "software engineering": "SE",
    "object oriented": "OOP",
    "artificial intelligence": "AI",
    "machine learning": "ML",
    "deep learning": "DL",
    "natural language": "NLP",
    "computer vision": "CV",
    "theory of computation": "TOC",
    "automata": "TOC",
    "compiler": "CD",
    "compiler design": "CD",
    "digital logic": "DLD",
    "digital circuit": "DLD",
    "microprocessor": "MP",
    "microcontroller": "MC",
    "embedded system": "ES",
    "signal and system": "SS",
    "signals and systems": "SS",
    "control system": "CS",
    "fluid mechanics": "FM",
    "engineering mathematics": "EM",
    "discrete mathematics": "DM",
    "discrete math": "DM",
    "linear algebra": "LA",
    "probability": "PS",
    "statistics": "PS",
    "probability and statistics": "PS",
    "engineering physics": "EP",
    "engineering chemistry": "EC",
    "web technology": "WT",
    "web development": "WD",
    "cryptography": "CNS",
    "network security": "CNS",
    "cyber security": "CS",
    "information security": "IS",
    "distributed system": "DS",
    "cloud computing": "CC",
    "big data": "BD",
    "data mining": "DM",
    "data warehousing": "DW",
    "human computer": "HCI",
    "mobile computing": "MC",
    "internet of things": "IoT",
    "image processing": "DIP",
    "digital image": "DIP",
    "graph theory": "GT",
    "numerical method": "NM",
    "advanced algorithm": "AA",
    "design and analysis": "DAA",
    "analysis of algorithm": "AOA",
    "design of algorithm": "DAA",
    "e-commerce": "EC",
    "electronic commerce": "EC",
    "management information": "MIS",
    "computer graphics": "CG",
    "computer science": "CS",
    "information technology": "IT",
    "electronics": "EC",
    "communication": "EC",
    "vlsi": "VLSI",
    "power system": "PS",
    "structural": "SA",
    "thermodynamics": "TD",
    "fluid": "FM",
    "solid mechanics": "SM",
    "manufacturing": "MP",
}


class Command(BaseCommand):
    help = "Auto-populate Subject.abbreviation for common CS/ECE subjects"

    def handle(self, *args, **options):
        updated = 0
        skipped = 0
        for subject in Subject.objects.all():
            if subject.abbreviation:
                skipped += 1
                continue  # never overwrite existing

            name_lower = subject.name.lower()
            matched_abbrev = None

            for keyword, abbrev in KNOWN_ABBREVS.items():
                if keyword in name_lower:
                    matched_abbrev = abbrev
                    break

            if matched_abbrev:
                subject.abbreviation = matched_abbrev
                subject.save(update_fields=["abbreviation"])
                self.stdout.write(
                    self.style.SUCCESS(f"  [OK]  {subject.name!r:50s} -> {matched_abbrev}")
                )
                updated += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f"  [?]  {subject.name!r} -- no abbreviation matched, set manually in admin")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Updated: {updated} subjects. Already filled / skipped: {skipped} subjects."
            )
        )

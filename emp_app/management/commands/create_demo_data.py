from django.core.management.base import BaseCommand

from emp_app.demo_data import seed_baseline
from emp_app.models import Employee


class Command(BaseCommand):
    help = "Creates a small set of demo departments/roles/employees if none exist."

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            default="default",
            help="Database alias to seed (default: 'default').",
        )

    def handle(self, *args, **options):
        db = options["database"]
        if Employee.objects.using(db).exists():
            self.stdout.write(f"Demo data skipped — employees already exist on '{db}'.")
            return

        seed_baseline(using=db)
        self.stdout.write(self.style.SUCCESS(f"Demo data created on '{db}'."))

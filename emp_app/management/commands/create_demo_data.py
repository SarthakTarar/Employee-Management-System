from datetime import date, timedelta

from django.core.management.base import BaseCommand

from emp_app.models import Department, Employee, Role


class Command(BaseCommand):
    help = "Creates a small set of demo departments/roles/employees if none exist."

    def handle(self, *args, **options):
        if Employee.objects.exists():
            self.stdout.write("Demo data skipped — employees already exist.")
            return

        engineering, _ = Department.objects.get_or_create(
            name="Engineering", defaults={"location": "Bengaluru"}
        )
        sales, _ = Department.objects.get_or_create(
            name="Sales", defaults={"location": "Mumbai"}
        )
        hr, _ = Department.objects.get_or_create(
            name="Human Resources", defaults={"location": "Delhi"}
        )

        developer, _ = Role.objects.get_or_create(name="Software Developer")
        manager, _ = Role.objects.get_or_create(name="Manager")
        recruiter, _ = Role.objects.get_or_create(name="Recruiter")

        today = date.today()
        demo_employees = [
            dict(
                first_name="Aditi",
                last_name="Rao",
                email="aditi.rao@example.com",
                phone="+91 90000 11111",
                dept=engineering,
                role=developer,
                salary=85000,
                bonus=5000,
                hire_date=today - timedelta(days=400),
            ),
            dict(
                first_name="Rohan",
                last_name="Mehta",
                email="rohan.mehta@example.com",
                phone="+91 90000 22222",
                dept=sales,
                role=manager,
                salary=95000,
                bonus=8000,
                hire_date=today - timedelta(days=20),
            ),
            dict(
                first_name="Priya",
                last_name="Nair",
                email="priya.nair@example.com",
                phone="+91 90000 33333",
                dept=hr,
                role=recruiter,
                salary=60000,
                bonus=2000,
                hire_date=today - timedelta(days=10),
            ),
        ]
        for data in demo_employees:
            Employee.objects.get_or_create(email=data["email"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Demo data created."))

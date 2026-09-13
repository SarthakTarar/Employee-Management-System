"""
Shared baseline dataset for demo/first-run seeding, used by both the
`create_demo_data` management command (default database, only if empty) and
the demo-account reset signals (demo database, unconditionally).
"""

from datetime import date, timedelta

from .models import Department, Employee, Role


def _baseline_employees(engineering, sales, hr, developer, manager, recruiter):
    today = date.today()
    return [
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


def seed_baseline(using="default"):
    """Creates the baseline departments/roles/employees on the given alias."""
    engineering, _ = Department.objects.using(using).get_or_create(
        name="Engineering", defaults={"location": "Bengaluru"}
    )
    sales, _ = Department.objects.using(using).get_or_create(
        name="Sales", defaults={"location": "Mumbai"}
    )
    hr, _ = Department.objects.using(using).get_or_create(
        name="Human Resources", defaults={"location": "Delhi"}
    )

    developer, _ = Role.objects.using(using).get_or_create(name="Software Developer")
    manager, _ = Role.objects.using(using).get_or_create(name="Manager")
    recruiter, _ = Role.objects.using(using).get_or_create(name="Recruiter")

    for data in _baseline_employees(
        engineering, sales, hr, developer, manager, recruiter
    ):
        Employee.objects.using(using).get_or_create(
            email=data["email"], defaults=data
        )


def reset_demo_database():
    """Wipes and reseeds the "demo" database back to the baseline dataset."""
    Employee.objects.using("demo").all().delete()
    Department.objects.using("demo").all().delete()
    Role.objects.using("demo").all().delete()
    seed_baseline(using="demo")

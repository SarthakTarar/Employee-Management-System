from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("department_list")


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("role_list")


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    dept = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="employees"
    )
    salary = models.PositiveIntegerField(default=0)
    bonus = models.PositiveIntegerField(default=0)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_absolute_url(self):
        return reverse("employee_detail", args=[self.pk])

    @property
    def total_pay(self):
        return self.salary + self.bonus

from django.contrib import admin

from .models import Department, Employee, Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name", "location")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "dept",
        "role",
        "salary",
        "bonus",
        "is_active",
        "hire_date",
    )
    list_filter = ("dept", "role", "is_active")
    search_fields = ("first_name", "last_name", "email", "phone")

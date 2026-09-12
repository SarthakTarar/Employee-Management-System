from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Employees
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path("employees/export/", views.employee_export_csv, name="employee_export"),
    path("employees/add/", views.EmployeeCreateView.as_view(), name="employee_add"),
    path(
        "employees/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
    path(
        "employees/<int:pk>/edit/",
        views.EmployeeUpdateView.as_view(),
        name="employee_edit",
    ),
    path(
        "employees/<int:pk>/delete/",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
    # Departments
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/add/",
        views.DepartmentCreateView.as_view(),
        name="department_add",
    ),
    path(
        "departments/<int:pk>/edit/",
        views.DepartmentUpdateView.as_view(),
        name="department_edit",
    ),
    path(
        "departments/<int:pk>/delete/",
        views.DepartmentDeleteView.as_view(),
        name="department_delete",
    ),
    # Roles
    path("roles/", views.RoleListView.as_view(), name="role_list"),
    path("roles/add/", views.RoleCreateView.as_view(), name="role_add"),
    path("roles/<int:pk>/edit/", views.RoleUpdateView.as_view(), name="role_edit"),
    path(
        "roles/<int:pk>/delete/",
        views.RoleDeleteView.as_view(),
        name="role_delete",
    ),
]

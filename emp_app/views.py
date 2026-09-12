import csv
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import DepartmentForm, EmployeeFilterForm, EmployeeForm, RoleForm
from .models import Department, Employee, Role


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = Employee.objects.all()
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        totals = employees.aggregate(
            payroll=Sum("salary"), bonus_total=Sum("bonus")
        )
        context.update(
            {
                "total_employees": employees.count(),
                "active_employees": employees.filter(is_active=True).count(),
                "total_departments": Department.objects.count(),
                "total_roles": Role.objects.count(),
                "total_payroll": (totals["payroll"] or 0) + (totals["bonus_total"] or 0),
                "recent_hires": employees.filter(hire_date__gte=thirty_days_ago).count(),
                "latest_employees": employees.order_by("-created_at")[:5],
            }
        )
        return context


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        qs = Employee.objects.select_related("dept", "role")
        self.filter_form = EmployeeFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            q = self.filter_form.cleaned_data.get("q")
            dept = self.filter_form.cleaned_data.get("dept")
            role = self.filter_form.cleaned_data.get("role")
            status = self.filter_form.cleaned_data.get("status")
            if q:
                qs = qs.filter(
                    Q(first_name__icontains=q)
                    | Q(last_name__icontains=q)
                    | Q(email__icontains=q)
                )
            if dept:
                qs = qs.filter(dept=dept)
            if role:
                qs = qs.filter(role=role)
            if status == "active":
                qs = qs.filter(is_active=True)
            elif status == "inactive":
                qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["querystring"] = self.request.GET.urlencode()
        return context


@login_required
def employee_export_csv(request):
    qs = Employee.objects.select_related("dept", "role")
    filter_form = EmployeeFilterForm(request.GET or None)
    if filter_form.is_valid():
        q = filter_form.cleaned_data.get("q")
        dept = filter_form.cleaned_data.get("dept")
        role = filter_form.cleaned_data.get("role")
        status = filter_form.cleaned_data.get("status")
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
            )
        if dept:
            qs = qs.filter(dept=dept)
        if role:
            qs = qs.filter(role=role)
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Department",
            "Role",
            "Salary",
            "Bonus",
            "Hire Date",
            "Status",
        ]
    )
    for emp in qs:
        writer.writerow(
            [
                emp.first_name,
                emp.last_name,
                emp.email or "",
                emp.phone,
                emp.dept.name,
                emp.role.name,
                emp.salary,
                emp.bonus,
                emp.hire_date,
                "Active" if emp.is_active else "Inactive",
            ]
        )
    return response


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Added {self.object} to the team.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Employee"
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Updated {self.object}.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit {self.object}"
        return context


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = "employees/employee_confirm_delete.html"
    success_url = reverse_lazy("employee_list")

    def form_valid(self, form):
        messages.success(self.request, f"Removed {self.object} from the team.")
        return super().form_valid(form)


# ---- Department CRUD ----

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "departments/department_list.html"
    context_object_name = "departments"


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    success_url = reverse_lazy("department_list")

    def form_valid(self, form):
        messages.success(self.request, f"Added department {form.instance.name}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Department"
        return context


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    success_url = reverse_lazy("department_list")

    def form_valid(self, form):
        messages.success(self.request, f"Updated department {self.object.name}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit {self.object.name}"
        return context


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = "departments/department_confirm_delete.html"
    success_url = reverse_lazy("department_list")

    def form_valid(self, form):
        messages.success(self.request, f"Removed department {self.object.name}.")
        return super().form_valid(form)


# ---- Role CRUD ----

class RoleListView(LoginRequiredMixin, ListView):
    model = Role
    template_name = "roles/role_list.html"
    context_object_name = "roles"


class RoleCreateView(LoginRequiredMixin, CreateView):
    model = Role
    form_class = RoleForm
    template_name = "roles/role_form.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        messages.success(self.request, f"Added role {form.instance.name}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Role"
        return context


class RoleUpdateView(LoginRequiredMixin, UpdateView):
    model = Role
    form_class = RoleForm
    template_name = "roles/role_form.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        messages.success(self.request, f"Updated role {self.object.name}.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit {self.object.name}"
        return context


class RoleDeleteView(LoginRequiredMixin, DeleteView):
    model = Role
    template_name = "roles/role_confirm_delete.html"
    success_url = reverse_lazy("role_list")

    def form_valid(self, form):
        messages.success(self.request, f"Removed role {self.object.name}.")
        return super().form_valid(form)

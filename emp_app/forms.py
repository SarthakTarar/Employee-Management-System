from django import forms

from .models import Department, Employee, Role


def _control(attrs=None, **extra):
    base = {"class": "form-control"}
    if attrs:
        base.update(attrs)
    base.update(extra)
    return base


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "dept",
            "role",
            "salary",
            "bonus",
            "hire_date",
            "is_active",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs=_control()),
            "last_name": forms.TextInput(attrs=_control()),
            "email": forms.EmailInput(attrs=_control()),
            "phone": forms.TextInput(attrs=_control(placeholder="+1 555 000 1234")),
            "dept": forms.Select(attrs=_control(**{"class": "form-select"})),
            "role": forms.Select(attrs=_control(**{"class": "form-select"})),
            "salary": forms.NumberInput(attrs=_control(min=0)),
            "bonus": forms.NumberInput(attrs=_control(min=0)),
            "hire_date": forms.DateInput(attrs=_control(type="date")),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class EmployeeFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs=_control(placeholder="Search by name or email…")
        ),
    )
    dept = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.all(),
        label="Department",
        widget=forms.Select(attrs=_control(**{"class": "form-select"})),
    )
    role = forms.ModelChoiceField(
        required=False,
        queryset=Role.objects.all(),
        label="Role",
        widget=forms.Select(attrs=_control(**{"class": "form-select"})),
    )
    status = forms.ChoiceField(
        required=False,
        label="Status",
        choices=[("", "All"), ("active", "Active"), ("inactive", "Inactive")],
        widget=forms.Select(attrs=_control(**{"class": "form-select"})),
    )


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "location"]
        widgets = {
            "name": forms.TextInput(attrs=_control()),
            "location": forms.TextInput(attrs=_control()),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs=_control()),
        }

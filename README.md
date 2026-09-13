# Employee Management System

A Django app for managing employees, departments, and roles — login-gated,
searchable, exportable, and ready to deploy to Vercel with Postgres (Neon).

## Features
- Dashboard with live stats (headcount, payroll, recent hires)
- Full CRUD for Employees, Departments, and Roles (the original only had
  add/remove/filter for employees — edit and department/role management are
  new)
- Search + filter (name/email, department, role, active status), paginated
- CSV export of the filtered employee list
- Session-based login required for every page; Django admin for superusers
- Environment-driven settings (`SECRET_KEY`, `DEBUG`, `DATABASE_URL`, …) so
  the same codebase runs locally on SQLite and in production on Postgres

## Try it live
**https://employee-management-system-two-livid.vercel.app**

Public demo login (view/add/edit/delete freely — this account's data lives on
an isolated database branch that resets to the baseline 3 departments/roles/
employees every time it logs in or out, so nothing you do there is permanent
or affects anyone else):
- Username: `demo`
- Password: `Orbit5965!`

## Local setup
```bash
python -m venv venv
./venv/Scripts/activate        # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py create_demo_data   # optional demo data
python manage.py runserver
```
Visit http://127.0.0.1:8000 and sign in.

## Project layout
- `emp_app/` — models, views (class-based), forms, admin, URLs, the
  `create_demo_data`/`create_demo_user` management commands
- `emp_app/db_router.py`, `emp_app/middleware.py`, `emp_app/signals.py` — the
  public demo account's isolated database routing + auto-reset
- `office_emp_m/` — Django project settings/urls/wsgi
- `templates/` — `base.html` + per-model templates (Bootstrap 5)
- `static/css/theme.css` — the custom design layer on top of Bootstrap
- `api/index.py`, `vercel.json`, `build_files.sh` — Vercel deployment wiring

## Deploying
See [DEPLOYMENT.md](DEPLOYMENT.md) for the full Vercel + Neon Postgres
walkthrough.

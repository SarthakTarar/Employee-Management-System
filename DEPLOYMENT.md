# Deploying to Vercel

Vercel runs Django as a serverless Python function. That means two things
this project is already set up for:

- **No persistent disk** → the database must be a real network database
  (Postgres), not SQLite. We use [Neon](https://neon.tech) (free tier).
- **No shell access after deploy** → one-off commands like `migrate` or
  `createsuperuser` must be run from your machine, pointed at the production
  database, not "on the server."

## 1. Create the Neon Postgres database
1. Sign up at https://neon.tech and create a new project/database.
2. Copy the connection string it gives you (starts with `postgresql://`).
   Make sure it includes `?sslmode=require`.

## 2. Configure environment variables in Vercel
In your Vercel project → **Settings → Environment Variables**, add:

| Key | Value |
|---|---|
| `SECRET_KEY` | a long random string (e.g. `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DEBUG` | `False` |
| `DATABASE_URL` | the Neon connection string from step 1 |
| `DATABASE_SSL_REQUIRE` | `True` |
| `ALLOWED_HOSTS` | `your-project.vercel.app` (add your custom domain too, comma-separated) |
| `CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app` |

## 3. Run migrations against the production database (from your machine)
```bash
# Temporarily point your local .env / shell at the Neon URL:
export DATABASE_URL="postgresql://...neon connection string..."
export DATABASE_SSL_REQUIRE=True

python manage.py migrate
python manage.py createsuperuser
python manage.py create_demo_data   # optional, only if the DB is empty
```

## 3b. Set up the public demo account (optional but recommended if you're
sharing the link)
Every logged-in account has full CRUD access — no view-only tier exists yet —
so a public demo account shares its data with a second, isolated Neon branch
instead of your real one, and that branch gets wiped back to a fixed baseline
every time the demo account logs in or out.

1. In the Neon dashboard, **Branches → Create branch** off your main branch,
   name it e.g. `demo`. Copy its connection string.
2. Add to Vercel's env vars: `DEMO_DATABASE_URL` (that connection string) and
   `DEMO_DATABASE_SSL_REQUIRE=True`.
3. From your machine, seed it and create the login (the demo branch is a
   *clone* of your main branch at creation time, so reset it rather than
   relying on `create_demo_data`'s "only if empty" check):
   ```bash
   export DEMO_DATABASE_URL="postgresql://...demo branch connection string..."
   python manage.py shell -c "from emp_app.demo_data import reset_demo_database; reset_demo_database()"

   export DATABASE_URL="postgresql://...your real connection string..."
   DEMO_USER_PASSWORD="pick-a-password" python manage.py create_demo_user
   ```
   `create_demo_user` always writes to the **default** database — the demo
   account's login itself isn't isolated, only its employee/department/role
   data is (see `emp_app/db_router.py` and `emp_app/signals.py`).
4. Put the username/password in your README (or wherever you share the link)
   so visitors can actually log in.

## 4. Deploy
Either:
- Push this repo to GitHub and import it in the Vercel dashboard (it will
  read `vercel.json` and `build_files.sh` automatically), or
- Use the CLI from the project root:
  ```bash
  npm i -g vercel
  vercel login
  vercel --prod
  ```

`vercel.json` builds `api/index.py` (the WSGI entrypoint) with
`@vercel/python`, runs `build_files.sh` to install dependencies and collect
static files into `staticfiles/`, and routes `/static/*` there while
everything else goes to Django.

## 5. Re-deploying after model changes
Whenever you change `models.py`, generate the migration locally
(`python manage.py makemigrations`), commit it, then repeat step 3's
`migrate` against the Neon URL before/after your Vercel deploy — Vercel won't
run it for you automatically.

## Notes / limitations
- File uploads (e.g. employee photos) aren't supported out of the box —
  Vercel's filesystem is wiped between invocations. Add S3/Cloudinary/Neon's
  own storage if you need that later.
- Cold starts: the first request after idle time will be slower while the
  serverless function spins up.

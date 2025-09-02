
# Paws & Walks — Final + Requests CRUD (Django 4.2 LTS)

This package contains the working version we validated together.
**Code is unchanged**, only the setup docs and requirements were adjusted
so it runs on your current macOS Python.

## What we adjusted
- Pinned **Django 4.2 LTS** (compatible with Python 3.9+).
- Created the **`static/`** folder to silence `STATICFILES_DIRS` warnings.
- Documented the correct **migration order** when using a custom `User` model
  (`accounts` first) to avoid `InconsistentMigrationHistory`.
- All instructions below are in English.

---

## Quickstart

From the project root (this folder), run:

```bash
# 1) Create & activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 2) Install deps (Django 4.2 LTS + Pillow)
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3) Go into the Django project folder
cd pawsproject

# 4) Make migrations (IMPORTANT: include accounts first)
python manage.py makemigrations accounts marketplace requestsboard

# 5) Apply migrations
python manage.py migrate

# 6) (Optional) Create an admin user
python manage.py createsuperuser

# 7) Run
python manage.py runserver
```

Open http://127.0.0.1:8000/

---

## Apps & Features

- **accounts**: Custom user (`@eafit.edu.co` email validation).
- **marketplace**: Seeder profile (photo upload), services & prices, ratings
  (create / edit / delete).
- **requestsboard**: Service Requests with Bootstrap cards (list, search,
  create, **My requests**, edit, delete). Navbar includes the **📡 Requests** link.
- Navbar brand logo is slightly larger.

---

## Troubleshooting

### A) No such table: `marketplace_sitterprofile`
Run migrations exactly as in step 4 & 5. If the DB existed before those steps,
delete it and try again:

```bash
# Stop the server (Ctrl + C), then from the 'pawsproject' folder:
rm -f db.sqlite3

# (Optional) clean previous migration files generated locally
find accounts -path "*/migrations/*.py" -not -name "__init__.py" -delete
find marketplace -path "*/migrations/*.py" -not -name "__init__.py" -delete
find requestsboard -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Recreate and apply
python manage.py makemigrations accounts marketplace requestsboard
python manage.py migrate
```

### B) InconsistentMigrationHistory (admin applied before accounts)
This happens if you migrated before creating `accounts` migrations. Use the same
reset steps above (delete `db.sqlite3`, optionally clean local migration files,
then run `makemigrations` with `accounts` first).

### C) STATICFILES_DIRS warning (W004)
We ship a `pawsproject/static/` directory. If you ever remove it, recreate it:

```bash
mkdir -p pawsproject/static
```

---

## Project tree (top level)

```
PawsAndWalks_Complete/
├─ README.md
├─ requirements.txt
└─ pawsproject/
   ├─ manage.py
   ├─ pawsproject/
   ├─ accounts/
   ├─ marketplace/
   ├─ requestsboard/
   ├─ templates/
   ├─ static/
   └─ media/
```

Enjoy! 🐾


# Setup Commands (exact sequence we used)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cd pawsproject
# IMPORTANT: create migrations including accounts first (custom user model)
python manage.py makemigrations accounts marketplace requestsboard
python manage.py migrate

python manage.py createsuperuser  # optional
python manage.py runserver
```

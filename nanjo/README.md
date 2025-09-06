# Nanjo Global Logistics Limited - Mini CRM & Website

## Setup

1. Create and activate venv (already created as `.venv`).
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create `.env` in project root with:

```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=nanjo_db
POSTGRES_USER=nanjo_user
POSTGRES_PASSWORD=nanjo_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

4. Run migrations and create superuser:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: /admin
CRM: /crm/
Public pages: /, /about/, /services/, /contact/

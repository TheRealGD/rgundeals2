rgundeals2 is a new site based on the [Django](https://www.djangoproject.com/) Python framework being developed as a backup to the primary project. Please ping stretch85 with questions/comments.

### Environment Setup

1. Set up a local PostgreSQL database and user.

```
CREATE DATABASE rgundeals;
CREATE USER rgundeals WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE rgundeals TO rgundeals;
```

2. Create `rgundeals/rgundeals/configuration.py` (same directory as `settings.py`) and define the following [Django settings](https://docs.djangoproject.com/en/dev/ref/settings/).

```
DEBUG = True
SECRET_KEY = '<secret-key>'
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rgundeals',
        'USER': 'rgundeals',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
    }
}
```

3. Install required Python packages.


```
pip install -r requirements.txt
```

4. Run database migrations.

```
./manage.py migrate
```

5. Create a superuser account.

```
./manae.py createsuperuser
```

6. Run the development server and access the web UI at <http://localhost:8000/>.

```
./manage.py runserver
```

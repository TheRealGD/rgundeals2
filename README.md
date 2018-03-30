rgundeals2 is a new site based on the [Django](https://www.djangoproject.com/) Python framework being developed as a backup to the primary project. Please ping stretch85 with questions/comments.

### Environment Setup

1. Ensure you have a virtual environment is setup and python 3 (virtualenvwrapper is your friend).

```
mkvirtualenv rgundeals2 -p python3
python --version
```

2. Install required Python packages.

```
pip install -r requirements.txt
```

3. Run database migrations.

```
./manage.py migrate
```

4. Create a superuser account.

```
./manae.py createsuperuser
```

5. Export variables for your development environment (DJ_DEBUG and DATABASE_URL if needed)

```
export DJ_DEBUG=True
export DATABASE_URL=postgres://USER:PW@HOST:5432/DB_NAME
```

6. Run the development server and access the web UI at <http://localhost:8000/>.

```
./manage.py runserver
```

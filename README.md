rgundeals2 is a new site based on the [Django](https://www.djangoproject.com/) Python framework being developed as a backup to the primary project. Please ping stretch85 with questions/comments.

### Housekeeping
We use a "develop" branch for changes and master is production pushes. We roughly follow the git pattern Vincent outlines [in this blog post](http://nvie.com/posts/a-successful-git-branching-model/), with focus on keeping the branches fairly clean.


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


### Development Server
The builtin django server requires debugging to be enabled for serving static files, so make sure to export DJ_DEBUG when running the builtin server.

1. Run the development server and access the web UI at <http://localhost:8000/>.

```
export DJ_DEBUG=True
./manage.py runserver
```

### Pre-staging/Heroku testing
We use dokku for the pushing the application, but you can use the heroku client to simulate the environment.

1. Setup environment for testing with heroku client

```
echo "DJ_DEBUG=True" >> .env
```

2. Run heroku locally (this will not work if you don't have DJ_DEBUG enabled)

```
heroku local
```

### Setting up dokku to push

1. Add dokku as a remote :

```
git 
```
import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Debugging settings, export the DJ_DEBUG if you need to enable debugging (SHOULD NEVER BE ON IN PROD!)
DEBUG = os.environ.get('DJ_DEBUG', 'False').lower() == 'true'

# SECRET KEY SHOULD ALWAYS BE CHANGED IN PROD!
SECRET_KEY = os.environ.get('DJ_SECRET_KEY', 'CHANGEME!!!')

# Allowed domain names
# TODO: change to a DJ_HOSTS variable
ALLOWED_HOSTS = ['*']

# For emailing errors
ADMINS = (('root', 'root@localhost'), )

INSTALLED_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'debug_toolbar',
    'bootstrap4',
    'mptt',

    # Local
    'users',
    'deals',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'rgundeals.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rgundeals.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Custom user model
AUTH_USER_MODEL = 'users.User'


# Set the default DB up, but use dj_database_url to pull the DATABASE_URL from the ENV variable
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'project-static'),
)

# Django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# django-bootstrap4
BOOTSTRAP4 = {
    'required_css_class': 'font-weight-bold',
}

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200

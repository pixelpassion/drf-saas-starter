import environ

env = environ.Env()                             # set default values and casting
environ.Env.read_env('.env')                    # reading .env file

root = environ.Path(__file__) - 2
ROOT_DIR = root()
MAIN_DIR = root.path('main')

DEBUG = env.bool('DEBUG', False)                # don't run with debug turned on in production ==> Default=False
STAGE = env.str('STAGE')                        # Every environment needs to set the stage

SECRET_KEY = env('SECRET_KEY')                  # Raises ImproperlyConfigured exception if SECRET_KEY not set
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])   # Should have '*' for local, the site URL for production

SITE_ID = 1

# Heroku expects to receive error messages on STDERR, the following logging takes care of this

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',

    'whitenoise.runserver_nostatic',   # use whitenoise for development , add above django.contrib.staticfiles
    'django.contrib.staticfiles',

    'apps.users',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

]

if DEBUG is True and STAGE == 'local':
        INSTALLED_APPS += [
            'django_extensions'
        ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(root.path('templates'))],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database

DATABASES = {
    'default': env.db(),                        # Raises ImproperlyConfigured exception if not set
}


# Password validation

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

# Authentication

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',            # Needed to login by username in Django admin, regardless of `allauth`
    'allauth.account.auth_backends.AuthenticationBackend',  # for specific authentication methods, such as login by e-mail
)

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

MEDIA_ROOT = str(root.path('media'))
MEDIA_URL = '/media/'
STATIC_ROOT = str(root.path('staticfiles'))
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    str(root.path('static')),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Mail handling

SENDGRID_API_KEY=env("SENDGRID_API_KEY", default=None)


# Heroku

# heroku labs:enable runtime-dyno-metadata must have been run before + a new deploy
ON_HEROKU = env('HEROKU_APP_ID', default=False)

if ON_HEROKU:

    HEROKU_RELEASE_CREATED_AT = env('HEROKU_RELEASE_CREATED_AT', default=None)
    HEROKU_RELEASE_VERSION = env('HEROKU_RELEASE_VERSION', default=None)
    HEROKU_SLUG_DESCRIPTION = env('HEROKU_SLUG_DESCRIPTION', default=None)
    HEROKU_SLUG_COMMIT = GIT_BRANCH = env('HEROKU_SLUG_COMMIT', default=None)

    SECURE_SSL_REDIRECT = True

    # In order to detect when a request is made via SSL in Django (for use in request.is_secure())
    # https://devcenter.heroku.com/articles/http-routing#heroku-headers

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Allauth

ACCOUNT_ALLOW_REGISTRATION = env.bool('ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ADAPTER = 'apps.users.adapters.AccountAdapter'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

AUTH_USER_MODEL = 'users.User'


#ACCOUNT_DEFAULT_HTTP_PROTOCOL="https"
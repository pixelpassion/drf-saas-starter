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
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
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
    'crispy_forms',
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


if DEBUG is True and STAGE == 'local':

        INSTALLED_APPS += [
            'django_extensions',
            'debug_toolbar',
        ]

        MIDDLEWARE = [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ] + MIDDLEWARE

        INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]


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

LANGUAGE_CODE = 'de-DE'
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

    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    MIDDLEWARE = [
        # We recommend putting this as high in the chain as possible
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    ] + MIDDLEWARE

    RAVEN_CONFIG = {
        'dsn': 'https://d8149058f0924193aa9af8a87e8dca83:fec43582f54b4c448882b44a7ce308a3@sentry.io/122593',
        'release': GIT_BRANCH
    }


# Allauth

ACCOUNT_ALLOW_REGISTRATION = env.bool('ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ADAPTER = 'apps.users.adapters.AccountAdapter'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

#ACCOUNT_DEFAULT_HTTP_PROTOCOL="https"

CRISPY_TEMPLATE_PACK = 'bootstrap4'


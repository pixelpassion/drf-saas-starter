import environ
import datetime
import sys

########################################################################################################################
#                                                            Index
########################################################################################################################

# 1     Basic
# 2     Installed apps + middleware
# 3     Templates + static files (CSS, JavaScript, Images)
# 4     Deployments (Heroku)
# *     Logging
# 5     Authentication
# 6     Mail handling
# 7     Celery
# 8     Django Rest Framework
# 9     Context (Admin, etc.)
# 10    Tenants


########################################################################################################################
#                                                      1 - Basics                                                      #
########################################################################################################################

env = environ.Env()                             # set default values and casting
environ.Env.read_env('.env')                    # reading .env file

root = environ.Path(__file__) - 2
ROOT_DIR = root()
MAIN_DIR = root.path('main')

DEBUG = env.bool('DEBUG', False)                            # debug should never be turned on in production
STAGE = env.str('STAGE')                                    # Every environment needs to set the stage

if sys.argv[1:2] == ['test']:
    STAGE = 'test'

SECRET_KEY = env('SECRET_KEY')                  # Raises ImproperlyConfigured exception if SECRET_KEY not set
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])   # Should have '*' for local, the site URL for production

SITE_ID = 1


ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'de_DE'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Everybody needs a database, Raises ImproperlyConfigured exception if not set
DATABASES = {
    'default': env.db(),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

# Lets cache some things

REDIS_URL = env.str('REDIS_URL', default=None)
CACHING = env.bool('CACHING', default=True)

if REDIS_URL and CACHING:

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': '{}/0'.format(REDIS_URL),
            'TIMEOUT': env.int('CACHE_TIMEOUT', default=86400),
        }
    }


########################################################################################################################
#                                            2 - Installed apps + Middleware                                           #
########################################################################################################################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',

    'whitenoise.runserver_nostatic',   # use whitenoise for development , add above django.contrib.staticfiles
    'django.contrib.staticfiles',

    'apps.tenants',
    'apps.users',
    'apps.mails',
    'apps.htmltopdf',
    
    'main.celery.CeleryConfig',
    'django_premailer', 

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    'oauth2_provider',
    'rest_framework_docs',
    'rest_framework_swagger',

    'django_extensions',        # This should be moved to only local, but it helps for testing
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'anymail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'apps.tenants.middleware.TenantMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG is True and STAGE == 'local':

        INSTALLED_APPS += [
            'debug_toolbar',
        ]

        MIDDLEWARE = [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        ] + MIDDLEWARE

        INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]


########################################################################################################################
#                                      3 - Templates + static files (CSS, JavaScript, Images)                          #
########################################################################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(root.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.admin_settings'
            ],
        },
    },
]

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

if not STAGE == 'test':
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


########################################################################################################################
#                                                4 - Deployments (Heroku)                                              #
########################################################################################################################

# heroku labs:enable runtime-dyno-metadata must have been run before + a new deploy
ON_HEROKU = env('HEROKU_APP_ID', default=False)

if ON_HEROKU:

    HEROKU_APP_NAME = env.str('HEROKU_APP_NAME')
    HEROKU_RELEASE_CREATED_AT = env('HEROKU_RELEASE_CREATED_AT', default=None)
    HEROKU_RELEASE_VERSION = env('HEROKU_RELEASE_VERSION', default=None)
    HEROKU_SLUG_DESCRIPTION = env('HEROKU_SLUG_DESCRIPTION', default=None)
    HEROKU_SLUG_COMMIT = GIT_BRANCH = env('HEROKU_SLUG_COMMIT', default=None)

    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

    # In order to detect when a request is made via SSL in Django (for use in request.is_secure())
    # https://devcenter.heroku.com/articles/http-routing#heroku-headers

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True    # https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SESSION_COOKIE_SECURE
    CSRF_COOKIE_HTTPONLY = True     # https://docs.djangoproject.com/en/1.10/ref/settings/#session-cookie-httponly
    CSRF_COOKIE_SECURE= True        # https://docs.djangoproject.com/en/1.10/ref/settings/#csrf-cookie-secure

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

    if CACHES:
        CACHES['default']['KEY_PREFIX'] = "{}-{}".format(HEROKU_APP_NAME, HEROKU_RELEASE_VERSION)



########################################################################################################################
#                                                Logging                                                               #
########################################################################################################################

if ON_HEROKU or STAGE in ['test', 'circleci']:

    # Heroku expects to receive error messages on STDERR, the following logging takes care of this
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry', ],
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

else:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s %(funcName)s()] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            },
            'django.db': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'WARNING',
            },
            'root': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'main': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }


########################################################################################################################
#                                                5 - Authentication                                                    #
########################################################################################################################

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
#ACCOUNT_DEFAULT_HTTP_PROTOCOL="https"

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',            # Needed to login by username in Django admin, regardless of `allauth`
    'allauth.account.auth_backends.AuthenticationBackend',  # for specific authentication methods, such as login by e-mail
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.7,
            'user_attributes': ('username', 'first_name', 'last_name', 'email')
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # optional path for password black list (default path: django/contrib/auth/common-passwords.txt.gz)
        'OPTIONS': {
            #'password_list_path': '/path/to/passwordBlackList.txt.gz',
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]


########################################################################################################################
#                                                6 - Mail handling                                                     #
########################################################################################################################

SENDGRID_API_KEY = env("SENDGRID_API_KEY", default=None)

if ON_HEROKU:

    ANYMAIL = {
        "SENDGRID_API_KEY": SENDGRID_API_KEY,
    }

    EMAIL_BACKEND = env('EMAIL_BACKEND', default='anymail.backends.sendgrid.SendGridBackend')

else:

    EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_PORT = env("EMAIL_PORT", default=1025)
    EMAIL_HOST = env("EMAIL_HOST", default='localhost')
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default='')
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default='')
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)

DEFAULT_FROM_EMAIL = "mail@example.org"

CRISPY_TEMPLATE_PACK = 'bootstrap4'


########################################################################################################################
#                                                 7 - Celery                                                           #
########################################################################################################################

# Settings should be moved to the new lowercase format
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#new-lowercase-settings

CELERY_BROKER_URL = env.str('CLOUDAMQP_URL', default='amqp://guest:guest@127.0.0.1')
BROKER_POOL_LIMIT = 1                   # Will decrease connection usage
BROKER_HEARTBEAT = None                 # We're using TCP keep-alive instead
BROKER_CONNECTION_TIMEOUT = 30          # May require a long timeout due to Linux DNS timeouts etc
CELERY_RESULT_BACKEND = None            # AMQP is not recommended as result backend as it creates thousands of queues
CELERY_SEND_EVENTS = False              # Will not create celeryev.* queues
CELERY_EVENT_QUEUE_EXPIRES = 60         # Will delete all celeryev. queues without consumers after 1 minute.


# When the setting CELERY_ALWAYS_EAGER is set to True, will all taskes be executed locally by blocking until the task
# returns. That is, tasks will be executed locally instead of being sent to the queue. This forces all calls to
# .delay()/.apply_async() that would normally get delegated to the worker to instead execute synchronously.
if STAGE == 'local':
    CELERY_TASK_ALWAYS_EAGER = env.bool('CELERY_ALWAYS_EAGER', default=True)


########################################################################################################################
#                                                 8 - Django Rest Framework                                            #
########################################################################################################################

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'oauth2_provider.ext.rest_framework.OAuth2Authentication',
#     ),
#     # 'DEFAULT_PERMISSION_CLASSES': (
#     #     'rest_framework.permissions.IsAuthenticated',
#     # )
# }

# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'api.exceptions.basic_exception_handler',
#
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'api.authentication.TokenAuthentication',
#     ),
#     'DEFAULT_PAGINATION_CLASS':
#         'api.pagination.StandardResultsSetPagination'
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_SECRET = env('JWT_SECRET')       # Raises ImproperlyConfigured exception if JWT_SECRET not set
JWT_ISSUER_NAME = env.str('JWT_ISSUER_NAME', default='einhorn-starter')

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'apps.api.jwt.payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.api.jwt.response_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'apps.api.jwt.get_username_from_payload_handler',
    'JWT_SECRET_KEY': JWT_SECRET,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60*60*72),
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=60*60*12),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ISSUER': 'einhorn-starter',
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
        'special_admin': 'Access to all data ressources'
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 12

}

REST_USE_JWT = True


########################################################################################################################
#                                             9 - Context (Admin, etc.)                                                #
########################################################################################################################

PROJECT_NAME = env.str('PROJECT_NAME', default='Untitled Project')

SENTRY_URL = env.str('SENTRY_URL', default="#")
MAILHOG_URL = env.str('MAILHOG_URL', default="#")
RABBITMQ_MANAGEMENT_URL = env.str('RABBITMQ_MANAGEMENT_URL', default="#")


########################################################################################################################
#                                                 10 - Tenants                                                         #
########################################################################################################################

ALLOWED_EMAIL_DOMAINS = [
    'jensneuhaus.de',
]

TENANT_DOMAIN = env.str('TENANT_DOMAIN', default='localhost:8000')

DEFAULT_DOMAINS = env.list('DEFAULT_DOMAINS',default=[
    'www.localhost:8000',
    '127.0.0.1:8000',
])
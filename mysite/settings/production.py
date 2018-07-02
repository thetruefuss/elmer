import os

from django.contrib.messages import constants as messages
from django.core.urlresolvers import reverse_lazy

import dj_database_url
from decouple import Csv, config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


LOGIN_REDIRECT_URL=reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL= reverse_lazy('logout')


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
    }


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'throttle',
    'frontboard',
    'user_accounts',
    'django.contrib.humanize',
    'crispy_forms',
    'feedback_form',
    'contact_form',
    'sorl.thumbnail',
    'messenger',

    'rest_framework',

    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'emoticons',
)

# Throttle
THROTTLE_ZONES = {
    'default': {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL':40,  # Period of time to enforce limits.
        'BUCKET_CAPACITY':10,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },
    'strict': {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,
        'BUCKET_INTERVAL':40,
        'BUCKET_CAPACITY':5,
    },
    'full_strict': {
        'VARY':'throttle.zones.RemoteIP',
        'NUM_BUCKETS':2,
        'BUCKET_INTERVAL':300,
        'BUCKET_CAPACITY':10,
    },
}
# Where to store request counts.
THROTTLE_BACKEND = 'throttle.backends.cache.CacheBackend'

# Force throttling when DEBUG=True
THROTTLE_ENABLED = True


#crispy_forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

#custom authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'user_accounts.authentication.EmailAuthBackend',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
            ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default = config('DATABASE_URL')
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY')

EMAIL_USE_TLS = config('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = config('EMAIL_BACKEND')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

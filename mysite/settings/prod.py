#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .common import *  # noqa

# database settings
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}

# email settings
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = config('EMAIL_BACKEND')

# django-cors-headers settings
CORS_ORIGIN_WHITELIST = ('localhost:3000', )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .common import *  # noqa

# database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-cors-headers settings
CORS_ORIGIN_WHITELIST = ('localhost:3000', )

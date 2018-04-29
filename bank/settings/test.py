import os
from decouple import config

from .base import *  # noqa: F403,F401

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, config('TEST_DB')),
        'USER': config('TEST_DB_USER'),
    }
}

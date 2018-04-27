import os
from decouple import config

from .base import * 

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, config('TEST_DB')),
        'USER': config('TEST_DB_USER'),
    }
}
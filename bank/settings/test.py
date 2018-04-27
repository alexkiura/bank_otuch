import os
from decouple import config

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, config('TEST_DB')),
        'USER': config('TEST_DB_USER'),
    }
}
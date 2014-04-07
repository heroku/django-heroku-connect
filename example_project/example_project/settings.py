import os
import sys

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPO_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.insert(0, REPO_DIR)

SECRET_KEY = 'sgw5-1k$ci949y)i9r9#$&=+^sev@a!pr-o766pzcjo0$hqzso'
INSTALLED_APPS = (
    'connect_client',
)

HEROKU_CONNECT_DATABASE_URL = os.environ['HEROKU_CONNECT_DATABASE_URL']
HEROKU_CONNECT_SCHEMA = os.environ['HEROKU_CONNECT_SCHEMA']
DATABASES = {
    'default': dj_database_url.config(default=HEROKU_CONNECT_DATABASE_URL),
}

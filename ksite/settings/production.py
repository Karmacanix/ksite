from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['serene-bayou-31914.herokuapp.com']

# need to call environment variables in this file
# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# secret key
SECRET_KEY = os.environ['SECRET_KEY'],
# i don't need an emailer

#disable collectstatic
#heroku config:set DISABLE_COLLECTSTATIC=0


try:
    from .local import *
except ImportError:
    pass

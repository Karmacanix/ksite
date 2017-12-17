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
SECRET_KEY = 'pgwrjx8!i96wla1hr1*1wj0ibmhrpfbk6-!n5&27g5zl7gw-af'

try:
    from .local import *
except ImportError:
    pass

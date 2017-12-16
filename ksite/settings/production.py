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
AWS_STORAGE_BUCKET_NAME = 'karmacanix2'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = 'AKIAJGKG6BOE2HJRC52A'
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME 

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#disable collectstatic
heroku config:set DISABLE_COLLECTSTATIC=1
#heroku config:set DISABLE_COLLECTSTATIC=0


try:
    from .local import *
except ImportError:
    pass

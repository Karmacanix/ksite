from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pgwrjx8!i96wla1hr1*1wj0ibmhrpfbk6-!n5&27g5zl7gw-af'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ksite',
        'USER': 'postgres',
        'PASSWORD': 'Rambo8731',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_STORAGE_BUCKET_NAME = 'karmastatix2'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = 'AKIAJGKG6BOE2HJRC52A'
AWS_SECRET_ACCESS_KEY = 'RJbPV1xdB+Tz0+ppcULPslQ5R6mX8h5HWPE6Ypgy'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME 

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



try:
    from .local import *
except ImportError:
    pass

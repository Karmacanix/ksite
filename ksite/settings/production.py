from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False


# need to call environment variables in this file
# database

# secret key

# i don't need an emailer



try:
    from .local import *
except ImportError:
    pass

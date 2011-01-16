"""
django-lumberjack
~~~~~~

`django-lumberjack <http://www.github.com/kevin/django-lumberjack>` provides a simple backport of some of hte logging fucntionality available in django 1.3.  It additionally provides a number of useful middlewares useful during debugging/development.

:copyright: Public Domain
"""


import os

import logging

try:
    from logging.config import dictConfig
except ImportError:
    from lumberjack.dictconfig import dictConfig
    
from lumberjack import settings

default_loggers = ['django.db.sql', 'django.db.summary', 
                   'django.request.ajax', 'django.request.profile.garbage', 
                   'django.request.profile.summary', 'django.request.profile.memory',
                   'django.request.session', 'django.cache']

if settings.LOGGING and settings.LOGGING.has_key('loggers'):
    dictConfig(settings.LOGGING)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = logging.getLogger('django')
if not logger.handlers:
    logger.addHandler(NullHandler())
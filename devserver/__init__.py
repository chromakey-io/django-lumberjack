"""
django-devserver
~~~~~~

`django-devserver <http://www.github.com/dcramer/django-devserver>` is a package
that aims to replace the built-in runserver command by providing additional
functionality such as real-time SQL debugging.

:copyright: 2010 by David Cramer
"""

__all__ = ('__version__', '__build__', '__docformat__', 'get_revision')
__version__ = (0, 0, 3)
__docformat__ = 'restructuredtext en'

import os

import logging

from devserver.dictconfig import dictConfig
from devserver import settings

default_loggers = ['django.db.sql', 'django.db.summary', 
                   'django.request.ajax', 'django.request.profile.garbage', 
                   'django.request.profile.summary', 'django.request.profile.memory',
                   'django.request.session', 'django.cache']

if settings.LOGGING and settings.LOGGING.has_key('loggers'):
    dictConfig(settings.LOGGING)

# sets a NullHandler for all the default loggers
# this prevents warnings when you call a logger 
# that hasn't been instantiated
class NullHandler(logging.Handler): 
    def emit(self, record): 
        pass
for logger in default_loggers:
    if logger not in settings.LOGGING['loggers'].keys():
        logger = logging.getLogger(logger)
        logger.addHandler(NullHandler())
        logger.propogate = False

def _get_git_revision(path):
    revision_file = os.path.join(path, 'refs', 'heads', 'master')
    if not os.path.exists(revision_file):
        return None
    fh = open(revision_file, 'r')
    try:
        return fh.read()
    finally:
        fh.close()

def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, '..'))
    path = os.path.join(checkout_dir, '.git')
    if os.path.exists(path):
        return _get_git_revision(path)
    return None

__build__ = get_revision()
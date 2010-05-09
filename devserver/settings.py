from django.conf import settings

DEVSERVER_TRUNCATE_SQL = getattr(settings, 'DEVSERVER_TRUNCATE_SQL', True)

DEVSERVER_TRUNCATE_AGGREGATES = getattr(settings, 'DEVSERVER_TRUNCATE_AGGREGATES', getattr(settings, 'DEVSERVER_TRUNCATE_AGGREGATES', False))

# This variable gets set to True when we're running the devserver
DEVSERVER_ACTIVE = False

DEVSERVER_AJAX_CONTENT_LENGTH = getattr(settings, 'DEVSERVER_AJAX_CONTENT_LENGTH', 300)

# Minimum time a query must execute to be shown, value is in MS
DEVSERVER_SQL_MIN_DURATION = getattr(settings, 'DEVSERVER_SQL_MIN_DURATION', None)

LOGGING = {
    'formatters': {
        'default' : {
            'format' : '[%(name)s] %(levelname)s %(message)s',
        },
    },
    'handlers' : {
        'stream' : {
            'class' : 'logging.StreamHandler',
            'formatter' : 'default',
            'level' : 'NOTSET',
        },
    },
    'loggers' : {
        'django' : {
            'level' : 'DEBUG',
            'handlers' : ['stream'],   #add additional handlers here (ie:email)
        },
    },
}

LOGGING = getattr(settings, 'LOGGING', LOGGING)
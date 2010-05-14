from django.conf import settings

LOGGING = {
    'formatters': {
        'error':{
            '()':'devserver.formatters.tb.TracebackFormatter',
            },
        'sql' : {
            '()':'devserver.formatters.sql.SQLFormatter',
            'format':'[%(name)s] %(levelname)s (%(duration)sms) %(message)s',
        },
        'default' : {
            'format' : '[%(name)s] %(levelname)s %(message)s',
        },
    },
    'handlers' : {
        'sqlstream' : {
            'class' : 'logging.StreamHandler',
            'formatter' : 'sql',
        },
        'errorstream' : {
            'class' : 'logging.StreamHandler',
            'formatter' : 'error',
            },
        'stream' : {
            'class' : 'logging.StreamHandler',
            'formatter' : 'default',
        },
    },
    'loggers' : {
        'django.db' : {
            'level' : 'DEBUG',
            'handlers' : ['sqlstream'],   #add additional handlers here (ie:email)
            },
        'django.errors' : {
            'level' : 'DEBUG',
            'handlers' : ['errorstream'],   #add additional handlers here (ie:email)
            },
        },
}

LOGGING = getattr(settings, 'LOGGING', LOGGING)
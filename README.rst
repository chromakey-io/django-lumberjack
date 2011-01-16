-----
About
-----

This is a logging server that tries to follow best practices with django and python.

It is highly customizable.  All included modules are optional, and follow with best practices of established tools it utilizes.  The entry-points for the loggers in django occur entirely through middlewares.  The loggers are designed around python's feature rich logging system rather than built from scratch.

*new support for arecibo.. woohoo!*

------------
Installation
------------

To install the latest stable version::

	pip install git+git://github.com/kevin/django-lumberjack#egg=django-lumberjack


django-lumberjack has some optional dependancies, which we highly recommend installing for development.

* ``pip install sqlparse`` -- pretty SQL formatting
* ``pip install pygments`` -- highlights tracebacks and sql

* ``pip install werkzeug`` -- interactive debugger
* ``pip install guppy`` -- tracks memory usage (required for MemoryUseModule)

You will need to include ``lumberjack`` in your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
	    'lumberjack',
	    ...
	)

Specify modules to load via the ``MIDDLEWARE_CLASSES`` setting::

	MIDDLEWARE_CLASSES = (
        # only available with DEBUG=True
        'lumberjack.middleware.sql.RealTime',
        'lumberjack.middleware.sql.Summary',

        'lumberjack.middleware.profile.Summary',
        'lumberjack.middleware.profile.UncollectedGarbage',
        'lumberjack.middleware.profile.MemoryUse',

        'lumberjack.middleware.request.SessionInfo',

        'lumberjack.middleware.ajax.Dump',

        'lumberjack.middleware.cache.Summary',
	)

----------------
500 Handler
----------------

Put this in your urls to get tracebacks to log.  This is here rather than a middleware, so that you can log middleware exceptions.
This only will work when DEBUG=False due to the way django handles exceptions.

handler500 = "lumberjack.views.server_error"

-----
Usage
-----

There is the same rundevserver command as available in the devserver app...

Though all of the middlewares will work regardless of which server you are running, the rundevserver command really only provides weurkzeug integration.

	python manage.py rundevserver

Note: This will force ``settings.DEBUG`` to ``True``.

This is necessary only if you want to use workzeug.  All of the middlewares will work with the regular runserver.
=======
Though with DEBUG = True you will lose the 500 handler.


-------
Modules
-------

The modules are the same as the devserver, only the have been implemented as middleware and simplified.

lumberjack.middleware.sql.RealTime
  Outputs queries as they happen to the terminal, including time taken.

lumberjack.middleware.sql.Summary
  Outputs a summary of your SQL usage.

lumberjack.middleware.profile.Summary
  Outputs a summary of the request performance.

lumberjack.middleware.profile.MemoryUse
  Outputs a notice when memory use is increased (at the end of a request cycle).

lumberjack.middleware.cache.Summary
  Outputs a summary of your cache calls at the end of the request.

lumberjack.middleware.ajax.Dump
  Outputs the content of any AJAX responses

lumberjack.middleware.request.SessionInfo
  Outputs information about the current session and user.


----------------
Named Logging
----------------

This is really what lumberjack brings to the table. Let your imagination run wild with what the formatters and handlers will allow you to do... included are some simple examples. setting::

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,

            'formatters': {
                'error' : {
                    '()': 'lumberjack.formatters.tb.TracebackFormatter',
                    'output':'terminal',
                    'format' : ('%(client_ip)s - [%(date_time)s] - "%(request_method)s"'
                                '%(content_length)s [%(url)s] \n %(exc_text)s' ),
                },
                'sql' : {
                    '()':'lumberjack.formatters.sql.SQLFormatter',
                    'format':'[%(name)s] %(levelname)s (%(duration)sms) %(message)s',
                    'output':'terminal',
                },
                'ajax' : {
                    '()':'lumberjack.formatters.ajax.AjaxFormatter',
                    'format':'[%(name)s] %(levelname)s %(message)s',
                    'output':'terminal',
                },
                'default' : {
                    'format' : '[%(name)s] %(levelname)s %(message)s',
                },
            },
            'handlers' : {
                'errorstream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'error',
                    },
                'sqlstream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'sql',
                    },
                'ajaxstream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'ajax',
                    },
                'stream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'default',
                },
                #'errorarecibo' : {
                #    'class' : 'lumberjack.handlers.AreciboHandler',
                #    'server': 'http://your-arebico-instance.appspot.com/',
                #    'account': 'public_account_password',
                #    },
                # requires python-arecibo lib
            },
            'loggers' : {
                'django.db' : {
                    'level' : 'DEBUG',
                    'handlers' : ['sqlstream'],
                    },
                'django.errors' : {
                    'level' : 'DEBUG',
                    'handlers' : ['errorstream'],
                    },
                'django.ajax' :{
                    'level' : 'DEBUG',
                    'handlers' : ['ajaxstream'],
                    },
                'django.profile' :{
                    'level' : 'DEBUG',
                    'handlers' : ['stream'],
                    },
                'django.cache' :{
                    'level' : 'DEBUG',
                    'handlers' : ['stream'],
                    },
                'django.request' :{
                    'level' : 'DEBUG',
                    'handlers' : ['stream'],
                    },
                },
        }

That seems pretty complex... but what it does is worth it.

Basically each middleware will write to its own named logger.  
If you include a middleware, but don't setup a logger for it or one of its parents it will write to a null logger.

Above, we have two loggers set-up.  The 'django.db' logger will catch everything that falls into that set  (ie: 'django.db.sql', 'django.db.summary').

The stream handler is built into python logging and will log to stderr... we are also using named handlers here for the purpose of setting a specific formatter for each.

Currently, lumberjack has the django specific handlers from jogging (which need testing and what-not).  

It also includes two formatters that both will format either for terminal use, or as HTML.
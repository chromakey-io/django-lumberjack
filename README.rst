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
* ``pip install werkzeug`` -- interactive debugger
* ``pip install guppy`` -- tracks memory usage (required for MemoryUseModule)
* ``pip install pygments`` --highlights tracebacks and sql

You will need to include ``lumberjack`` in your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
	    'lumberjack',
	    ...
	)

Specify modules to load via the ``MIDDLEWARE_CLASSES`` setting::

	  (
	    'lumberjack.middleware.sql.SQLRealTimeModule',
	    'lumberjack.middleware.sql.SQLSummaryModule',
	    'lumberjack.middleware.profile.ProfileSummaryModule',

	    # Modules not enabled by default
	    'lumberjack.middleware.ajax.AjaxDumpModule',
	    'lumberjack.middleware.profile.MemoryUseModule',
	    'lumberjack.middleware.cache.CacheSummaryModule',
	)

----------------
500 Handler
----------------

Put this in your urls to get tracebacks to log.  This is here rather than a middleware, so that you can log middleware exceptions.

handler500 = "lumberjack.views.server_error"

-----
Usage
-----

As with the devserver app there is...

	python manage.py rundevserver

Note: This will force ``settings.DEBUG`` to ``True``.

This is necessary only if you want to use workzeug.  All of the middlewares will work with the regular runserver.

-------
Modules
-------

The modules are the same as the devserver, only the have been implemented as middleware and simplified.

lumberjack.middleware.sql.SQLRealTimeModule
  Outputs queries as they happen to the terminal, including time taken.

lumberjack.middleware.sql.SQLSummaryModule
  Outputs a summary of your SQL usage.

lumberjack.middleware.profile.ProfileSummaryModule
  Outputs a summary of the request performance.

lumberjack.middleware.profile.MemoryUseModule
  Outputs a notice when memory use is increased (at the end of a request cycle).

lumberjack.middleware.cache.CacheSummaryModule
  Outputs a summary of your cache calls at the end of the request.

lumberjack.middleware.ajax.AjaxDumpModule
  Outputs the content of any AJAX responses

lumberjack.middleware.request.SessionInfoModule
  Outputs information about the current session and user.


----------------
Named Logging
----------------

This is really what lumberjack brings to the table.  setting::

        LOGGING = {
            'formatters': {
                'errorterminal':{
                    '()':'lumberjack.formatters.tb.TracebackFormatter',
                    'output':'terminal',
                    },
                'sql' : {
                    '()':'lumberjack.formatters.sql.SQLFormatter',
                    'output':'terminal',
                    'format':'[%(name)s] %(levelname)s (%(duration)sms) %(message)s',
                },
                'default' : {
                    'format' : '[%(name)s] %(levelname)s %(message)s',
                },
            },
            'handlers' : {
                'erroremail' : {
                    'class' : 'lumberjack.handlers.AdminEmailHandler',
                    },
                'errorstream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'errorterminal',
                    },
                'sqlstream' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'sql',
                    },
                },
            },
            'loggers' : {
                'django.db' : {
                    'level' : 'DEBUG',
                    'handlers' : ['sqlstream'],
                    },
                'django.errors' : {
                    'level' : 'DEBUG',
                    'handlers' : ['errorstream','erroremail'],
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
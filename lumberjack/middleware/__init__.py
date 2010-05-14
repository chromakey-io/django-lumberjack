import logging

class LoggingMiddleware(object):
    """
    Functions a lot like middleware, except that it does not accept any return values.
    """
    logger_name = 'django'
    
    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
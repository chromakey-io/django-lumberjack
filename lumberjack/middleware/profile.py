from lumberjack.middleware import LoggingMiddleware
from lumberjack.utils.time import ms_from_timedelta

from datetime import datetime

import gc

class ProfileSummary(LoggingMiddleware):
    """
    Outputs a summary of cache events once a response is ready.
    """

    logger_name = 'django.request.profile.summary'
    
    def process_request(self, request):
        self.start = datetime.now()

    def process_response(self, request, response):
        duration = datetime.now() - self.start
        
        self.logger.info('Total time to render was %.2fs', ms_from_timedelta(duration) / 1000)
        return response

class UncollectedGarbage(LoggingMiddleware):
    """
    Outputs a summary of events the garbage collector couldn't handle.
    """
    # TODO: Not even sure this is correct, but the its a general idea

    logger_name = 'django.request.profile.garbage'
    
    def process_request(self, request):
        gc.enable()
        gc.set_debug(gc.DEBUG_SAVEALL)

    def process_response(self, request, response):
        gc.collect()
        self.logger.info('%s objects left in garbage', len(gc.garbage))
        return response

from django.template.defaultfilters import filesizeformat

try:
    from guppy import hpy
except ImportError:
    import warnings

    class MemoryUseModule(LoggingMiddleware):
        def __new__(cls, *args, **kwargs):
            warnings.warn('MemoryUseModule requires guppy to be installed.')
            return super(MemoryUseModule, cls).__new__(cls)
else:
    class MemoryUse(LoggingMiddleware):
        """
        Outputs a summary of memory usage of the course of a request.
        """
        logger_name = 'django.request.profile.memory'
    
        def process_request(self, request):
            from guppy import hpy
        
            self.usage = 0

            self.heapy = hpy()
            self.heapy.setrelheap()

        def process_response(self, request, response):
            h = self.heapy.heap()
        
            if h.domisize > self.usage:
                self.usage = h.domisize
        
            if self.usage:
                self.logger.info('Memory usage was increased by %s', filesizeformat(self.usage))
            return response

from lumberjack.middleware import LoggingMiddleware
from lumberjack import settings

class Dump(LoggingMiddleware):
    """
    Dumps the content of all AJAX responses.
    """

    logger_name = LoggingMiddleware.logger_name + '.ajax'
    
    def process_response(self, request, response):
        if request.is_ajax():
            # Let's do a quick test to see what kind of response we have
            self.logger.info(response.content)
        return response
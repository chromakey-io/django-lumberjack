from devserver.middleware import LoggingMiddleware
from devserver import settings

class AjaxDump(LoggingMiddleware):
    """
    Dumps the content of all AJAX responses.
    """

    logger_name = LoggingMiddleware.logger_name + '.ajax'
    
    def process_response(self, request, response):
        if request.is_ajax():
            # Let's do a quick test to see what kind of response we have
            if len(response.content) < settings.DEVSERVER_AJAX_CONTENT_LENGTH:
                self.logger.info(response.content)
        return response
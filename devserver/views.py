from django.conf import settings
from django import http
from django.template import RequestContext, loader
import sys

import logging

def server_error(request, template_name='500.html'):
    """

    500 error handler.
    """

    t = loader.get_template(template_name)

    logger = logging.getLogger('django.errors')
    logger.error("Uncaught Exception", exc_info=True)

    return http.HttpResponseServerError(t.render(RequestContext(request)))
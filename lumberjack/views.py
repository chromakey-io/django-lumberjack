from django.conf import settings
from django import http
from django.template import RequestContext, loader
import sys

import logging

def server_error(request, template_name='500.html'):
    """

    500 error handler.
    """

    logger = logging.getLogger('django.errors')

    msg = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)

    try:
        request_repr = repr(request)
    except:
        request_repr = "Request repr() unavailable"

    logger.error(msg, exc_info=True, extra = {'request_repr':request_repr, 'url':request.build_absolute_uri()})

    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request)))
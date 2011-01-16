from django.conf import settings
from django import http
from django.template import RequestContext, loader

from datetime import datetime

import sys
import logging

def server_error(request, template_name='500.html'):
    """

    500 error handler.
    """

    logger = logging.getLogger('django.errors')
    msg = "Error: "

    logger.error(msg, exc_info=True, extra = {'client_ip':request.META.get('REMOTE_ADDR'), 'date_time':datetime.now(),
        'url':request.build_absolute_uri(), 'request_method':request.META.get('REQUEST_METHOD'),
        'content_length':request.META.get('CONTENT_LENGTH')})

    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request)))
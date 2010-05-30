import datetime, logging
import os

HOST = os.uname()[1]

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

class MockHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.msgs = []
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.msgs.append(record)

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from lumberjack.models import Log
        
        msg = self.format(msg)
        
        if hasattr(record, 'request_repr'):
            request_repr = record.request_repr
        else:
            request_repr = "Request repr() unavailable"
        
        try:
            Log.objects.create(request_repr=request_repr, level=record.levelname, msg=msg)
        except:
            # squelching exceptions sucks, but 500-ing because of a logging error sucks more
            pass

class AdminEmailHandler(logging.Handler):
    def emit(self, record):
        from django.core.mail import mail_admins
        
        # call the formatter to have it format and append the traceback to the record.message
        msg = self.format(record)
        
        # the subject should be the msg before the traceback is appended
        subject = record.msg
        
        if hasattr(record, 'request_repr'):
            request_repr = record.request_repr
        else:
            request_repr = "Request repr() unavailable"
        
        msg = "%s\n\n%s" % (msg, request_repr)

        mail_admins(subject, msg, fail_silently=True)
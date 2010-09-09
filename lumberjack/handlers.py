import datetime, logging
import os

HOST = os.uname()[1]

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

class AreciboHandler(logging.Handler):
    def __init__(self, server, account):
        self.server = server
        self.account = account
        
        logging.Handler.__init__(self)
        
    def emit(self, record):
        from arecibo import post
        
        msg = self.format(record)
        
        if hasattr(record, 'request_repr'):
            request_repr = record.request_repr
        else:
            request_repr = "Request repr() unavailable"
        
        if hasattr(record, 'url'):
            url = record.url
        else:
            url = ''
        
        try:
            arecibo = post()
            arecibo.server(url=self.server)
            arecibo.set("account", self.account)
            arecibo.set("status", "500")
            arecibo.set("url", url)
            arecibo.set("traceback", msg)
            arecibo.send()
        except:
            # squelching exceptions sucks, but 500-ing because of a logging error sucks more
            pass

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from lumberjack.models import Log
        
        msg = self.format(record)
        
        if hasattr(record, 'request_repr'):
            request_repr = record.request_repr
        else:
            request_repr = "Request repr() unavailable"
        
        if hasattr(record, 'url'):
            url = record.url
        else:
            url = ''
        
        try:
            Log.objects.create(request_repr=request_repr, url=url, level=record.levelname, msg=msg)
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
        
        if hasattr(record, 'url'):
            subject = record.url + ' ' + subject

        msg = "%s\n\n%s" % (msg, request_repr)

        mail_admins(subject, msg, fail_silently=True)
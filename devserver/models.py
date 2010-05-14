import datetime
from django.db import models

class Log(models.Model):
    "A log message, used by jogging's DatabaseHandler"
    datetime = models.DateTimeField(default=datetime.datetime.now)
    level = models.CharField(max_length=128)
    msg = models.TextField()
    source = models.CharField(max_length=128, blank=True)
    host = models.CharField(max_length=200, blank=True, null=True)

    def abbrev_msg(self, maxlen=500):
        if len(self.msg) > maxlen:
            return u'%s ...' % self.msg[:maxlen]
        return self.msg
    abbrev_msg.short_description = u'abbreviated msg'
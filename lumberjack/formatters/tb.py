import logging
import sqlparse
import re

from pygments import highlight
from pygments.lexers import PythonTracebackLexer
from pygments.formatters import TerminalFormatter, HtmlFormatter

import cStringIO, traceback

class TracebackFormatter:
    def __init__(self, fmt=None, output='terminal'):
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument (if omitted, you get the ISO8601 format).
        """
        if fmt:
            self._fmt = fmt
        else:
            self._fmt = "%(message)s %(exc_text)s"

        if output == 'html':
            self.formatter = HtmlFormatter()
        elif output == 'terminal':
            self.formatter = TerminalFormatter()
        else:
            self.formatter = NullFormatter()

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        sio = cStringIO.StringIO()
        traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

    def format(self, record):
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        record.exc_text = highlight(record.exc_text, PythonTracebackLexer(), self.formatter)

        record.message = record.getMessage()
        message = self._fmt % record.__dict__
        
        return message
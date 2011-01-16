import logging
import sqlparse
import re

from pygments import highlight
from pygments.lexers import JavascriptLexer
from pygments.formatters import TerminalFormatter, HtmlFormatter

import cStringIO, traceback

class AjaxFormatter:

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
            self._fmt = ""

        if output == 'html':
            self.formatter = HtmlFormatter()
        elif output == 'terminal':
            self.formatter = TerminalFormatter()
        else:
            self.formatter = NullFormatter()

    def format(self, record):
        message = record.getMessage()
        sql_fields_re = re.compile(r'SELECT .*? FROM')
        message = sql_fields_re.sub('SELECT ... FROM', message)
        message = sqlparse.format(message, reindent=True, keyword_case='upper')
        
        record.message = ''
        
        header = self._fmt % record.__dict__
        
        if not isinstance(self.formatter, HtmlFormatter):
            indent = ' ' * (len(header) + 1)
            
            formatted_message = []
            first = True
            for line in message.split('\n'):
                if first:
                    formatted_message.append(line)
                    first = False
                else:
                    formatted_message.append('%s%s' % (indent, line))
            message = '\n'.join(formatted_message)
        
        message = highlight(message, JavascriptLexer(), self.formatter)

        return header + message
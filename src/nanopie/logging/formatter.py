import json
import logging
import socket
from typing import Dict, Optional

from ..globals import logging_context, tracing_context

class DefaultLogRecordFormatter(logging.Formatter):
    """
    """
    def __init__(self,
                 fmt: Optional[Dict] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 flatten: bool = False,
                 merge_logging_context = False,
                 merge_tracing_context = False,
                 quiet: bool = True):
        """
        """
        super().__init__(fmt=None, datefmt=datefmt, style=style)

        hostname = socket.gethostname()
        if style == '{':
            self.__style = logging.StrFormatStyle
            default_fmt = {
                'host': '{}'.format(hostname),
                'logger': '{name}',
                'level': '{levelname}',
                'module': '{module}',
                'func': '{funcname}'
            }
        elif style == '$':
            self.__style = logging.StringTemplateStyle
            default_fmt = {
                'host': '{}'.format(hostname),
                'logger': '${name}',
                'level': '${level}',
                'module': '${module}',
                'func': '${func}'
            }
        elif style == '%':
            self.__style = None
            default_fmt = {
                'host': '{}'.format(hostname),
                'logger': '%(name)s',
                'level': '%(level)s',
                'module': '%(module)s',
                'func': '%(func)s'
            }
        
        self.__fmt = fmt if fmt else default_fmt
        self.flatten = flatten
        self.merge_logging_context = merge_logging_context
        self.merge_tracing_context = merge_tracing_context
        self.quiet = quiet

    def format(self, record: 'LogRecord'):
        """
        """
        super().format(record)

        dikt = {}

        for k in self.__fmt:
            try:
                if self.__style:
                    v = self.__style(self.__fmt[k]).format(record)
                else:
                    v = self.__fmt[k] % record.__dict__
                dikt[k] = v
            except KeyError as ex:
                if not self.quiet:
                    raise ex
        
        message = record.msg
        if isinstance(message, dict):
            dikt.update(message)
        else:
            dikt['message'] = super().format(record)

        if self.merge_logging_context:
            try:
                dikt.update(logging_context.to_dikt())
            except Exception as ex:
                if not self.quiet:
                    raise ex

        if self.merge_tracing_context:
            try:
                dikt.update(tracing_context.to_dikt())
            except Exception as ex:
                if not self.quiet:
                    raise ex

        if self.flatten:
            return json.dumps(dikt)
        
        return dikt

    def usesTime(self):
        """
        """
        if self.__style:
            search = self.__style.asctime_search
        else:
            search = "%(asctime)"

        return any([value.find(search) >= 0 for value in self.__fmt.values()])

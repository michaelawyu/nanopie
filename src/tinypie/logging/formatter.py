import logging
import socket
from typing import Dict

class DiktLogRecordFormatter(logging.Formatter):
    """
    """
    def __init__(self,
                 fmt:Optional[Dict] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
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
                'logger': '%{name}s',
                'level': '%{level}s',
                'module': '%{module}s',
                'func': '%{func}s'
            }
        
        self.__fmt = fmt if fmt else default_fmt
        self.quiet = quiet

    def format(self, record: 'LogRecord'):
        """
        """
        dikt = {}

        for k in self.__fmt:
            try:
                if self.__style:
                    v = self.__style(self.__fmt[k]).format(record)
                else:
                    v = self.__fmt[k] % record.__dict__
            except KeyError as ex:
                if not self.quiet:
                    raise ex

        # TO-DO: Merge log context

        return dikt


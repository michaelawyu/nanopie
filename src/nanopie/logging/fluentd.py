from typing import Dict, List, Optional

try:
    import fluent
    from fluent import handler as fluent_handler
    FLUENT_INSTALLED = True
except ImportError:
    FLUENT_INSTALLED = False

from .base import LoggingHandler
from .formatter import CustomLogRecordFormatter

class FluentdLoggingHandler(LoggingHandler):
    """
    """
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 24224,
                 tag: str = 'app',
                 **kwargs):
        """
        """
        if not FLUENT_INSTALLED:
            raise ImportError(
                'The fluent-logger (https://pypi.org/project/fluent-logger/)'
                'package is required to set up logging with Fluentd. To '
                'install this package, run `pip install fluent-logger`.')

        self._host = host
        self._port = port
        self._tag = tag

        super().__init__(**kwargs)
    
    def _setup_logger(self, logger: 'logging.Logger'):
        """
        """
        handler = fluent_handler.FluentHandler(tag=self._tag,
                                               host=self._host,
                                               port=self._port)
        formatter = CustomLogRecordFormatter(
            fmt=self._fmt,
            datefmt=self._datefmt,
            style=self._style,
            flatten=False,
            log_ctx_extractor=self._log_ctx_extractor,
            quiet=self._quiet)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self._level)

import logging
from typing import Dict, List, Optional

try:
    import fluent
    from fluent import handler
    FLUENT_INSTALLED = True
except ImportError:
    FLUENT_INSTALLED = False

from .base import LogHandlerWorkMode, LoggingConfiguration
from ..formatter import DefaultLogRecordFormatter

class FluentdLoggingConfiguration(LoggingConfiguration):
    """
    """
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 24224,
                 tag: str = 'app',
                 level: int = logging.INFO,
                 fmt: Optional[Dict] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 quiet: bool = True,
                 mode: int = LogHandlerWorkMode.SYNC,
                 merge_logging_context: bool = False,
                 merge_tracing_context: bool = False):
        """
        """
        if not FLUENT_INSTALLED:
            raise ImportError(
                'The fluent-logger (https://pypi.org/project/fluent-logger/)'
                'package is required to set up logging with Fluentd. To '
                'install this package, run `pip install fluent-logger`.')

        self.host = host
        self.port = port
        self.tag = tag

        super().__init__(level=level,
                         fmt=fmt,
                         datefmt=datefmt,
                         style=style,
                         quiet=quiet,
                         mode=mode,
                         merge_logging_context=merge_logging_context,
                         merge_tracing_context=merge_tracing_context)
    
    def _setup_logger(self, logger: 'logging.Logger'):
        """
        """
        log_handler = handler.FluentHandler(tag=self.tag,
                                            host=self.host,
                                            port=self.port)
        log_formatter = DefaultLogRecordFormatter(fmt=self.fmt,
                                                  datefmt=self.datefmt,
                                                  style=self.style,
                                                  flatten=False,
                                                  merge_logging_context=self.merge_logging_context,
                                                  merge_tracing_context=self.merge_tracing_context,
                                                  quiet=self.quiet)
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)
        logger.setLevel(self.level)

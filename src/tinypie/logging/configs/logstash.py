import logging
from typing import Dict, List, Optional

from .base import LogHandlerWorkMode, LoggingConfiguration
from ..formatter import DefaultLogRecordFormatter
from ..handlers.logstash import LogstashTCPHandler, LogstashUDPHandler

class LogstashLoggingConfiguration(LoggingConfiguration):
    """
    """
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 9600,
                 use_udp: bool = False,
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
        self.host = host
        self.port = port
        self.use_udp = use_udp

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
        if self.use_udp:
            log_handler = LogstashUDPHandler(host=self.host, port=self.port)
        else:
            log_handler = LogstashTCPHandler(host=self.host, port=self.port)

        log_formatter = DefaultLogRecordFormatter(fmt=self.fmt,
                                                  datefmt=self.datefmt,
                                                  style=self.style,
                                                  flatten=True,
                                                  merge_logging_context=self.merge_logging_context,
                                                  merge_tracing_context=self.merge_tracing_context,
                                                  quiet=self.quiet)
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)
        logger.setLevel(self.level)

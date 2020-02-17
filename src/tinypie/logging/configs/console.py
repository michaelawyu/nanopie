import logging
from typing import Dict, List, Optional

from .base import LogHandlerWorkMode, LoggingConfiguration
from ..formatter import DefaultLogRecordFormatter

class ConsoleLoggingConfiguration(LoggingConfiguration):
    """
    """
    def __init__(self,
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
        log_handler = logging.StreamHandler()
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

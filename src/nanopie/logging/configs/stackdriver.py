import logging
from typing import Any, BinaryIO, Dict, List, Optional, TextIO

try:
    from google.cloud import logging as stackdriver_logging
    STACKDRIVER_INSTALLED = True
except ImportError:
    STACKDRIVER_INSTALLED = False

from .base import LogHandlerWorkMode, LoggingConfiguration
from ..formatter import DefaultLogRecordFormatter
from ..handlers.stackdriver import (
    DEFAULT_LOGGER_NAME,
    StackdriverHandler,
    PatchedSyncTransport,
    _GLOBAL_RESOURCE
)

class LogstashLoggingConfiguration(LoggingConfiguration):
    """
    """
    def __init__(self,
                 client: 'stackdriver_logging.Client',
                 custom_log_name: Optional[str] = None,
                 resource: Optional['stackdriver_logging.resource.Resource'] = None,
                 labels: Optional[Dict] = None,
                 stream: Optional[Any[TextIO, BinaryIO]] = None,
                 level: int = logging.INFO,
                 fmt: Optional[Dict] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 quiet: bool = True,
                 mode: int = LogHandlerWorkMode.BACKGROUND_THREAD,
                 merge_logging_context: bool = False,
                 merge_tracing_context: bool = False,
                 **kwargs):
        """
        """
        if not STACKDRIVER_INSTALLED:
            raise ImportError(
                'The google-cloud-logging (https://pypi.org/project/google-cloud-logging/)'
                'package is required to set up logging with Stackdriver. To '
                'install this package, run `pip install google-cloud-logging`.')

        self.client = stackdriver_logging.Client(**kwargs)
        self.custom_log_name = custom_log_name if custom_log_name else DEFAULT_LOGGER_NAME
        self.resource = resource if resource else _GLOBAL_RESOURCE
        self.labels = labels
        self.stream = stream

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
        if self.mode == LogHandlerWorkMode.SYNC:
            log_handler = PatchedSyncTransport(client=self.client,
                                               name=self.custom_log_name)
        else:
            log_handler = StackdriverHandler(client=self.client,
                                             name=self.custom_log_name,
                                             resource=self.resource,
                                             labels=self.labels,
                                             stream=self.stream)

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

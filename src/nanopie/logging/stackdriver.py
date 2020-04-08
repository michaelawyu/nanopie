import logging
from typing import BinaryIO, Dict, Optional, TextIO, Union

try:
    from google.cloud import logging as stackdriver_logging
    STACKDRIVER_INSTALLED = True
except ImportError:
    STACKDRIVER_INSTALLED = False

from .base import LoggingHandlerModes, LoggingHandler
from .formatter import CustomLogRecordFormatter

try:
    from .handlers.stackdriver import (
        DEFAULT_LOGGER_NAME,
        StackdriverHandler,
        PatchedSyncTransport,
        _GLOBAL_RESOURCE,
    )
except:
    STACKDRIVER_INSTALLED = False


class StackdriverLoggingHandler(LoggingHandler):
    """
    """

    def __init__(
        self,
        client: "stackdriver_logging.Client",
        custom_log_name: Optional[str] = None,
        resource: Optional["stackdriver_logging.resource.Resource"] = None,
        labels: Optional[Dict] = None,
        stream: Optional[Union[TextIO, BinaryIO]] = None,
        **kwargs
    ):
        """
        """
        if not STACKDRIVER_INSTALLED:
            raise ImportError(
                "The google-cloud-logging "
                "(https://pypi.org/project/google-cloud-logging/)"
                "package is required to set up logging with Stackdriver. To "
                "install this package, run `pip install google-cloud-logging`."
            )

        self._client = stackdriver_logging.Client(**kwargs)
        self._custom_log_name = (
            custom_log_name if custom_log_name else DEFAULT_LOGGER_NAME
        )
        self._resource = resource if resource else _GLOBAL_RESOURCE
        self._labels = labels
        self._stream = stream

        super().__init__(**kwargs)

    def _setup_logger(self, logger: "logging.Logger"):
        """
        """
        if self._mode == LoggingHandlerModes.SYNC:
            handler = StackdriverHandler(
                client=self._client,
                name=self._custom_log_name,
                transport=PatchedSyncTransport,
                resource=self._resource,
                labels=self._labels,
                stream=self._stream,
            )
        else:
            handler = StackdriverHandler(
                client=self._client,
                name=self._custom_log_name,
                resource=self._resource,
                labels=self._labels,
                stream=self._stream,
            )

        formatter = CustomLogRecordFormatter(
            fmt=self._fmt,
            datefmt=self._datefmt,
            style=self._style,
            flatten=True,
            log_ctx_extractor=self._log_ctx_extractor,
            quiet=self._quiet,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self._level)

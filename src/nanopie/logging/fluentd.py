"""This module includes the logging handler for connecting to Fluentd services.
"""

try:
    from fluent import handler as fluent_handler

    FLUENT_INSTALLED = True
except ImportError:
    FLUENT_INSTALLED = False

from .base import LoggingHandler
from .formatter import CustomLogRecordFormatter


class FluentdLoggingHandler(LoggingHandler):
    """The logging handler for connecting to Fluentd services."""

    def __init__(
        self, host: str = "localhost", port: int = 24224, tag: str = "app", **kwargs
    ):
        """Initializes a Fluentd logging handler.

        Args:
            host (str): The hostname or address of the Fluentd service.
            port (int): The port of the Fluentd service.
            tag (str): The log entry tags.
            **kwargs: Other keyword arguments for logging handlers. See
                `LoggingHandler`.
        """
        if not FLUENT_INSTALLED:
            raise ImportError(
                "The fluent-logger (https://pypi.org/project/fluent-logger/)"
                "package is required to set up logging with Fluentd. To "
                "install this package, run `pip install fluent-logger`."
            )

        self._host = host
        self._port = port
        self._tag = tag

        super().__init__(**kwargs)

    def _setup_logger(self, logger: "logging.Logger"):
        """Sets up a logger.

        The logger is configured with a custom log formatter, which helps
        format structured logs, and a handler, which transmits logs to
        a Fluentd service.

        Args:
            logger ("Logger"): A logger.
        """
        handler = fluent_handler.FluentHandler(
            self._tag, host=self._host, port=self._port
        )
        formatter = CustomLogRecordFormatter(
            fmt=self._fmt,
            datefmt=self._datefmt,
            style=self._style,
            flatten=False,
            log_ctx_extractor=self._log_ctx_extractor,
            quiet=self._quiet,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self._level)

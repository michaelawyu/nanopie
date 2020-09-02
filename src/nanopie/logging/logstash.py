"""This module includes the logging handler for connecting to Logstash services.
"""

from .base import LoggingHandler
from .formatter import CustomLogRecordFormatter
from .handlers.logstash import LogstashTCPHandler, LogstashUDPHandler


class LogstashLoggingHandler(LoggingHandler):
    """The logging handler for connecting to Logstash services."""

    def __init__(
        self, host: str = "localhost", port: int = 9600, use_udp: bool = False, **kwargs
    ):
        """Initializes a Logstash logging handler.

        Args:
            host (str): The hostname or address of the Logstash service.
            port (int): The port of the Logstash service.
            use_udp (bool): If set to True, the logs will be transmitted using
                the UDP protocol.
            **kwargs: Other keyword arguments for logging handlers. See
                `LoggingHandler`.
        """
        self._host = host
        self._port = port
        self._use_udp = use_udp

        super().__init__(**kwargs)

    def _setup_logger(self, logger: "logging.Logger"):
        """Sets up a logger.

        The logger is configured with a custom log formatter, which helps
        format structured logs, and a logger, which transmits logs to
        a Logstash service.

        Args:
            logger ("Logger"): A logger.
        """
        if self._use_udp:
            handler = LogstashUDPHandler(host=self._host, port=self._port)
        else:
            handler = LogstashTCPHandler(host=self._host, port=self._port)

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

from .base import LoggingHandler
from .formatter import CustomLogRecordFormatter
from .handlers.logstash import LogstashTCPHandler, LogstashUDPHandler

class LogstashLoggingHandler(LoggingHandler):
    """
    """
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 9600,
                 use_udp: bool = False,
                 **kwargs):
        """
        """
        self._host = host
        self._port = port
        self._use_udp = use_udp

        super().__init__(**kwargs)
    
    def _setup_logger(self, logger: 'logging.Logger'):
        """
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
            quiet=self._quiet
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self._level)

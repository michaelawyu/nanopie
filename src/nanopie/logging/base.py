from abc import abstractmethod
import logging
from typing import Dict, List, Optional

from .formatter import CustomLogRecordFormatter
from ..globals import endpoint
from ..handler import Handler
from ..model import Model
from ..services.base import Extractor


class LogContext(Model):
    """
    """


class LogContextExtractor(Extractor):
    """
    """

    @abstractmethod
    def extract(self, request: "Request") -> "LogContext":
        """
        """


class LoggingHandlerModes:
    """
    """

    SYNC = 1
    BACKGROUND_THREAD = 2
    ASYNC = 3
    supported_modes = [SYNC, BACKGROUND_THREAD, ASYNC]


class LoggingHandler(Handler):
    """
    """
    def __init__(
        self,
        default_logger_name: str = __name__,
        span_name: str = 'unspecified_span',
        level: int = logging.INFO,
        fmt: Optional[Dict] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
        quiet: bool = True,
        mode: int = LoggingHandlerModes.SYNC,
        log_ctx_extractor: Optional[LogContextExtractor] = None,
    ):
        """
        """
        self._default_logger_name = default_logger_name
        self._span_name = span_name
        self._level = level
        self._fmt = fmt
        self._datefmt = datefmt
        self._style = style
        self._quiet = quiet
        if mode not in LoggingHandlerModes.supported_modes:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    LoggingHandlerModes.supported_modes
                )
            )
        self._mode = mode
        self._log_ctx_extractor = log_ctx_extractor
        self._default_logger = None

        super().__init__()

    def __call__(self, *args, **kwargs):
        """
        """
        logger = self.default_logger

        span_name = self._span_name
        if not span_name:
            span_name = endpoint.name

        entering = "Entering span {}.".format(span_name)
        exiting = "Exiting span {}.".format(span_name)

        logger.info(entering)
        res = super().__call__(*args, **kwargs)
        logger.info(exiting)
        return res

    def _setup_logger(self,
                      logger: "logging.Logger"):
        """
        """
        handler = logging.StreamHandler()
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

    def getLogger(self,
                  name: Optional[str] = None,
                  append_handlers: bool = False) -> "logging.Logger":
        """
        """
        if not name or name == 'root':
            raise ValueError(
                "To set up the root logger, use " "setup_root_logger method instead."
            )

        logger = logging.getLogger(name)

        if len(logger.handlers) == 0 or append_handlers:
            self._setup_logger(logger)
        else:
            raise RuntimeError('A logger with the given name already exists '
                               'and has one or more handlers configured.')

        return logger
    
    @property
    def default_logger(self) -> "logging.Logger":
        """
        """
        if not self._default_logger:
            self._default_logger = self.getLogger(self._default_logger_name)

        return self._default_logger

    def setup_root_logger(self,
                          excluded_loggers: List[str],
                          append_handlers: bool = False):
        """
        """
        root_logger = logging.getLogger()

        if len(root_logger.handlers) == 0 or append_handlers:
            self._setup_logger(root_logger)
        else:
            raise RuntimeError('The root logger already has one or more '
                               'handlers configured.')

        for name in excluded_loggers:
            logger = logging.getLogger(name)
            logger.propagate = False
            if not logger.hasHandlers():
                logger.addHandler(logging.lastResort)
        
        return root_logger

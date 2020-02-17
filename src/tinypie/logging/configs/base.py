from abc import abstractmethod, ABC
import logging
from typing import Dict, List, Optional

class LogHandlerWorkMode:
    SYNC = 1
    BACKGROUND_THREAD = 2
    ASYNC = 3

class LoggingConfiguration(ABC):
    """
    """
    _configured_loggers = []

    def __init__(self,
                 level: int = logging.INFO,
                 fmt: Optional[Dict] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 quiet: bool = True,
                 mode: int = LogHandlerWorkMode.SYNC,
                 merge_logging_context: bool = False,
                 merge_tracing_context: bool = False,
                 **kwargs):
        """
        """
        self.level = level
        self.fmt = fmt
        self.datefmt = datefmt
        self.style = style
        self.quiet = quiet
        self.mode = mode
        self.merge_logging_context = merge_logging_context
        self.merge_tracing_context = merge_tracing_context

    @abstractmethod
    def _setup_logger(self, logger: 'logging.Logger'):
        """
        """
        pass

    def getLogger(self, name: str) -> 'logging.Logger':
        """
        """
        logger = logging.getLogger(name)

        if name not in self._configured_loggers:
            self._setup_logger(logger)
            self._configured_loggers.append(name)

        return logger

    def setup_root_logger(self, excluded_loggers: List[str]):
        """
        """
        if 'root' not in self._configured_loggers:
            logger = logging.getLogger()
            self._setup_logger(logger)
            self._configured_loggers.append('root')
        
        for name in excluded_loggers:
            logger = logging.getLogger(name)
            logger.propagate = False
            logger.addHandler(logging.StreamHandler())

"""This module includes the base classes for logging handlers and related objects.

A logging handler enables easy and convenient Python idiomatic structured
logging. Once configured, it can help collect runtime information
(such as current stack frame, current time, and current module) and
request specific contexts (such as current user, and the source of the
request) and send them, along with custom messages, to a
source (standard streams, Fluentd, Logstash, Stackdriver, etc.) in the form
of structured payloads automatically. You can also add logging handlers
to an endpoint in a microservice/API service so that it can automatically
log the beginning and the end of the processing of a request.
"""

from abc import abstractmethod
import logging
from typing import Any, Dict, List, Optional

from .formatter import CustomLogRecordFormatter
from ..globals import endpoint, request
from ..handler import Handler
from ..model import Model
from ..services.base import Extractor


class LogContext(Model):
    """The base class for all log contexts.

    A log context is a `Model` (see `model.py`) that specifies a number of
    request specific attributes that logging handlers can access and add
    to log entries.

    For example, the frontend of an e-commerce system often adds the IDs of
    customers to requests, which the backend can use to tag the logs. With
    these tags, developers may group log entries by customers, making it
    easy to track customer activities.
    """


class LogContextExtractor(Extractor):
    """The base class for all log context extractors.

    A log context extractor extracts a log context from a request. For example,
    a log context extractor for an HTTP microservice/API service can read
    some HTTP headers and parse them into a log context which logging handlers
    can use.
    """

    @abstractmethod
    def extract(self, request: "RPCRequest") -> "LogContext":
        """Extracts a log context from a request.

        Args:
            request (RPCRequest): A request.

        Returns:
            LogContext: The extracted log context.
        """


class LoggingHandlerModes:
    """The modes which logging handlers use.

    nanopie logging handlers support three modes:
    - SYNC: Transmit logs synchronously.
    - BACKGROUND_THREAD: Transmit logs asynchonrously with a background thread.
    - ASYNC: Transmit logs asynchronously in an event loop. Note that this
        mode is only available when you use logging handlers in an asynchronous
        transport (e.g. quart).

    To-Do: These modes have not been implemented in logging handlers. The
    default logging handler (`LoggingHandler`), LogStash logging Handler, and
    Fluentd logging handler work synchronously regardless of the specified
    mode; Stackdriver logging handler, on the other hand, supports SYNC and
    BACKGROUND_THREAD modes at this moment.
    """

    SYNC = 1
    BACKGROUND_THREAD = 2
    ASYNC = 3
    supported_modes = [SYNC, BACKGROUND_THREAD, ASYNC]


class LoggingHandler(Handler):
    """The base class for all logging handlers.

    This logging handler can also be used directly if the
    microservice/API service requires only log outputs to standard streams
    (stdout/stderr).
    """

    def __init__(
        self,
        default_logger_name: str = __name__,
        span_name: str = "unspecified_span",
        level: int = logging.INFO,
        fmt: Optional[Dict] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
        quiet: bool = True,
        mode: int = LoggingHandlerModes.SYNC,
        log_ctx_extractor: Optional[LogContextExtractor] = None,
    ):
        """Initializes a logging handler.

        Args:
            default_logger_name (str): The name of the logger. Note that logger
                names are globally unique; see
                https://docs.python.org/3/library/logging.html for more
                information.
            span_name (str): The name of the span, usually the processing
                of a request. For example, if you set
                up a logging handler in an endpoint `get_user`, the span_name
                can be configured as `get_user` so that the logging
                handler will output a log message `Entering span get_user`
                when beginning processing a request to the `get_user` endpoint
                and a log message `Exiting span get_user` when finishing
                processing a request to the same endpoint.
            level (int): The log level. See
                https://docs.python.org/3/library/logging.html#logging-levels
                for more information.
            fmt (Dict, Optional): The format of the log. It is in the form
                of a Dict (instead of the default string) where logging
                handlers will attempt to automatically
                format the values using Python LogRecord attributes
                (https://docs.python.org/3/library/logging.html#logrecord-attributes)
                and extras
                (https://docs.python.org/3/library/logging.html#logging.Logger.debug)
                users provide (if any).
            datefmt (str): The format of date and time (if any) in the log.
                See also
                https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime.
            style (str): How the values in the fmt Dict are formatted. It
                can be one of the three values: `%`, `{`, and `$`.
                See also
                https://docs.python.org/3/library/logging.html#logging.Formatter.
            quiet (bool): If set to True, the logging handler runs quietly
                when extracting log contexts, i.e. it will not report any
                error should a log context cannot be extracted or processed.
            mode (int): The mode this logging handler uses.
            log_ctx_extractor (LogContextExtractor, Optional): A log context
                extractor.
        """
        self._fmt = fmt
        self._datefmt = datefmt
        self._style = style
        self._default_logger_name = default_logger_name
        self._span_name = span_name
        self._level = level
        if mode not in LoggingHandlerModes.supported_modes:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    LoggingHandlerModes.supported_modes
                )
            )
        self._mode = mode
        self._default_logger = None
        self._log_ctx_extractor = log_ctx_extractor
        self._quiet = quiet

        super().__init__()

    def __call__(self, *args, **kwargs) -> Any:
        """Runs the handler.

        It performs the following tasks:

        1. Set up a logger (if one has not been set up yet).
        2. Log the beginning of a span, such as the processing of a request.
        3. Pass the baton to the chained handler.
        4. Log the ending of the span.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary named arguments.

        Returns:
            Any: Any object.
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

    def get_log_ctx(self) -> "LogContext":
        """Gets the current log context.

        Returns:
            LogContext: The current log context.
        """
        if self._log_ctx_extractor:
            return self._log_ctx_extractor.extract(request=request)
        else:
            raise RuntimeError("log_ctx_extractor is not present.")

    def _setup_logger(self, logger: "logging.Logger"):
        """Sets up a logger.

        The logger is configured with a custom log formatter, which helps
        format structured logs, and a handler, which transmits logs to
        a standard stream.

        Args:
            logger ("Logger"): A logger.
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

    def getLogger(
        self, name: Optional[str] = None, append_handlers: bool = False
    ) -> "logging.Logger":
        """Gets a logger.

        Args:
            name (str, Optional): The name of the the logger.
            append_handlers (bool): If set to True, the logging handler
                will set up a logger even if the logger already has a
                handler specified. This may cause duplicate log entries
                if configured inappropriately.

        Returns
            Logger: A logger.
        """
        if not name or name == "root":
            raise ValueError(
                "To set up the root logger, use setup_root_logger method instead."
            )

        logger = logging.getLogger(name)

        if len(logger.handlers) == 0 or append_handlers:
            self._setup_logger(logger)
        else:
            raise RuntimeError(
                "A logger with the given name already exists "
                "and has one or more handlers configured."
            )

        return logger

    @property
    def default_logger(self) -> "logging.Logger":
        """Gets the default logger associated with the logging handler.

        Returns:
            Logger: A logger.
        """
        if not self._default_logger:
            self._default_logger = self.getLogger(self._default_logger_name)

        return self._default_logger

    def setup_root_logger(
        self, excluded_loggers: List[str], append_handlers: bool = False
    ) -> "logging.Logger":
        """Sets up the root logger.

        Args:
            excluded_loggers (List[str]): A list of loggers whose propagation
                will be disabled. This prevents error logs produced by
                errored handlers themselves being redirected back to these
                handlers.
            append_handlers (bool): If set to True, the logging handler
                will set up the root logger even if it already has a
                handler specified. This may cause duplicate log entries
                if configured inappropriately.

        Returns:
            Logger: A logger.
        """
        root_logger = logging.getLogger()

        if len(root_logger.handlers) == 0 or append_handlers:
            self._setup_logger(root_logger)
        else:
            raise RuntimeError(
                "The root logger already has one or more " "handlers configured."
            )

        for name in excluded_loggers:
            logger = logging.getLogger(name)
            logger.propagate = False
            if not logger.hasHandlers():
                logger.addHandler(logging.lastResort)

        return root_logger

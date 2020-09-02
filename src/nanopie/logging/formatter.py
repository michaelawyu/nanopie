import json
import logging
import socket
from typing import Dict, Optional

from ..globals import request
from ..logger import logger as package_logger


class CustomLogRecordFormatter(logging.Formatter):
    """The custom formatter for logging handlers."""

    def __init__(
        self,
        fmt: Optional[Dict] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
        flatten: bool = False,
        log_ctx_extractor: Optional["LogContextExtractor"] = None,
        quiet: bool = True,
    ):
        """Initializes a log formatter.

        Args:
            fmt (Dict, Optional): The format of the log. It is in the form
                of a Dict (instead of the default string) where logging
                handlers will attempt to automatically
                format the values using Python LogRecord attributes
                (https://docs.python.org/3/library/logging.html#logrecord-attributes)
                and extras
                (https://docs.python.org/3/library/logging.html#logging.Logger.debug)
                users provide (if any).
            datefmt (str, Optional): The formate of date and time (if any) in the log.
                See also
                https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime.
            style (str): How the values in the fmt Dict are formatted. It
                can be one of the three values: `%`, `{`, and `$`.
                See also
                https://docs.python.org/3/library/logging.html#logging.Formatter.
            flatten (bool): If set to True, the formatter will pass a
                serialized Dict to the handler.
            log_ctx_extractor (LogContextExtractor, Optional): A log context
                extractor.
            quiet (bool): If set to True, the logging handler runs quietly
                when extracting log contexts, i.e. it will not report any
                error should a log context cannot be extracted or processed.
        """
        super().__init__(fmt=None, datefmt=datefmt, style=style)

        hostname = socket.gethostname()
        if style == "{":
            self.__style = logging.StrFormatStyle
            default_fmt = {
                "host": "{}".format(hostname),
                "logger": "{name}",
                "level": "{levelname}",
                "module": "{module}",
                "func": "{funcName}",
            }
        elif style == "$":
            self.__style = logging.StringTemplateStyle
            default_fmt = {
                "host": "{}".format(hostname),
                "logger": "${name}",
                "level": "${levelname}",
                "module": "${module}",
                "func": "${funcName}",
            }
        elif style == "%":
            self.__style = None
            default_fmt = {
                "host": "{}".format(hostname),
                "logger": "%(name)s",
                "level": "%(levelname)s",
                "module": "%(module)s",
                "func": "%(funcName)s",
            }

        self.__fmt = fmt if fmt else default_fmt
        self._flatten = flatten
        self._quiet = quiet
        self._log_ctx_extractor = log_ctx_extractor

    def format(self, record: "LogRecord"):
        """See the method `logging.Formatter.format`."""
        super().format(record)

        dikt = {}

        for k in self.__fmt:
            try:
                if self.__style:
                    v = self.__style(self.__fmt[k]).format(record)
                else:
                    v = self.__fmt[k] % record.__dict__
                dikt[k] = v
            except KeyError as ex:
                if not self._quiet:
                    raise ex

        message = record.msg
        if isinstance(message, dict):
            dikt.update(message)
        else:
            dikt["message"] = super().format(record)

        if self._log_ctx_extractor:
            try:
                log_ctx = self._log_ctx_extractor.extract(request=request)
                log_ctx = log_ctx.to_dikt()
                for k in log_ctx:
                    dikt[k] = log_ctx[k]
            except Exception as ex:  # pylint: disable=broad-except
                if not self._quiet:
                    raise RuntimeError("Cannot extract log context {}.".format(str(ex)))

        if self._flatten:
            return json.dumps(dikt)

        return dikt

    def usesTime(self):
        """See the method `logging.Formatter.usesTime`."""
        if self.__style:
            search = self.__style.asctime_search
        else:
            search = "%(asctime)"

        return any([value.find(search) >= 0 for value in self.__fmt.values()])

import json
import logging
import socket
from typing import Dict, Optional

from ..globals import request
from ..logger import logger as package_logger


class CustomLogRecordFormatter(logging.Formatter):
    """
    """

    def __init__(
        self,
        fmt: Optional[Dict] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
        flatten: bool = False,
        log_ctx_extractor: Optional["LogContextExtractor"] = None,
        quiet: bool = True,
    ):
        """
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
        """
        """
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
                    raise RuntimeError("Cannot extract log context ().".format(str(ex)))

        if self._flatten:
            return json.dumps(dikt)

        return dikt

    def usesTime(self):
        """
        """
        if self.__style:
            search = self.__style.asctime_search
        else:
            search = "%(asctime)"

        return any([value.find(search) >= 0 for value in self.__fmt.values()])

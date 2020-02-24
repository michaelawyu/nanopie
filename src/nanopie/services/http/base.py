from abc import abstractmethod
from typing import Any, Callable, Dict, Optional

from ..base import RPCEndpoint, RPCRequest, RPCResponse, RPCService
from .foundation import HTTPFoundationHandler
from ...handler import SimpleHandler
from .methods import HTTPMethods
from ...serialization.http import HTTPSerializationHandler
from ...serialization.helpers.json import JSONSerializationHelper


class HTTPRequest(RPCRequest):
    """
    """

    __slots__ = (
        "_url",
        "_headers",
        "_content_length",
        "_mime_type",
        "_query_args",
        "_binary_data",
        "_text_data",
    )

    def __init__(
        self,
        url: Any[str, Callable],
        headers: Any[Dict, Callable],
        content_length: Any[int, Callable],
        mime_type: Any[str, Callable],
        query_args: Any[Dict, Callable],
        binary_data: Callable,
        text_data: Callable,
    ):
        """
        """
        self._url = url
        self._headers = headers
        self._content_length = content_length
        self._mime_type = mime_type
        self._query_args = query_args
        self._binary_data = binary_data
        self._text_data = text_data

    @staticmethod
    def _helper(v: Any) -> Any:
        """
        """
        if callable(v):
            return v()
        else:
            return v

    @property
    def url(self) -> str:
        return self._helper(self._url)

    @property
    def headers(self) -> Dict:
        return self._helper(self._headers)

    @property
    def content_length(self) -> int:
        return self._helper(self._content_length)

    @property
    def mime_type(self) -> str:
        return self._helper(self._mime_type)

    @property
    def query_args(self) -> Dict:
        return self._helper(self._query_args)

    @property
    def binary_data(self) -> bytes:
        return self._helper(self._binary_data)

    @property
    def text_data(self) -> str:
        return self._helper(self._text_data)


class HTTPParsedRequest:
    """
    """

    __slots__ = ("headers", "query_args", "data")

    def __init__(
        self,
        headers: Optional["Model"] = None,
        query_args: Optional["Model"] = None,
        data: Optional["Model"] = None,
    ):
        """
        """
        self.headers = headers
        self.query_args = query_args
        self.data = data


class HTTPResponse(RPCResponse):
    """
    """

    __slots__ = ("_status_code", "_headers", "_mime_type", "_data")

    def __init__(
        self,
        status_code: int = 200,
        headers: Optional[Any[Dict, "Model"]] = None,
        mime_type: Optional[str] = None,
        data: Optional[Any[str, bytes, "Model"]] = None,
    ):
        """
        """
        self._status_code = status_code
        self._headers = headers
        self._mime_type = mime_type
        self._data = data

    @property
    def status_code(self) -> int:
        """
        """
        if type(self._status_code) != int:
            raise RuntimeError(
                "HTTP Response must have a status code of " "the int type."
            )
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int):
        """
        """
        if type(status_code) != int:
            raise RuntimeError(
                "HTTP Response must have a status code of " "the int type."
            )
        self._status_code = status_code

    @property
    def headers(self) -> Dict:
        """
        """
        headers = self._headers
        if not headers:
            return {"Content-Type": self.mime_type}

        if type(self._headers) != dict:
            raise RuntimeError(
                "HTTP Response must have a dict as headers. "
                "If a response is initialized with a model "
                "as headers, a serializer must be present "
                "to serialize the model."
            )
        n = "Content-Type"
        for k in headers:
            if k.lower() == n.lower():
                n = k
        headers[n] = self.mime_type
        return headers

    @headers.setter
    def headers(self, headers: Optional[Dict]):
        """
        """
        if not headers:
            headers = {}

        if type(headers) != dict:
            raise RuntimeError("HTTP Response must have a dict as " "headers.")

        self._headers = headers

    @property
    def mime_type(self) -> str:
        """
        """
        if not self.mime_type:
            return ""

        if type(self._mime_type) != str:
            raise RuntimeError("The mime type must be a str.")

        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: Optional[str]):
        """
        """
        if not mime_type:
            mime_type = ""

        if type(mime_type) != str:
            raise RuntimeError("The mime type must be a str.")

        self._mime_type = mime_type

    @property
    def data(self) -> Optional[Any[str, bytes]]:
        """
        """
        if not self._data:
            return

        if type(self._data) not in [str, bytes]:
            raise RuntimeError(
                "HTTP Response must have a str or bytes as "
                "data. If a response is initialized with a "
                "model as data, a serializer must be present "
                "to serialize the model."
            )

        return self._data

    @data.setter
    def data(self, data: Optional[Any[str, bytes]]):
        """
        """
        if not data:
            self._data = None
            return

        if type(data) not in [str, bytes]:
            raise RuntimeError("HTTP Response must have a str or bytes as " "data.")

        self._data = data


class HTTPEndpoint(RPCEndpoint):
    """
    """

    def __init__(self, method: str, **kwargs):
        """
        """
        self.method = method

        super().__init__(**kwargs)


class HTTPService(RPCService):
    """
    """

    def __init__(
        self,
        serialization_handler: "SerializationHandler",  # To-Do
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        max_content_length: Optional[int] = 6000,
    ):
        """
        """
        super().__init__(
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            max_content_length=max_content_length,
        )

    @abstractmethod
    def add_endpoint(self, endpoint: "HTTPEndpoint", **kwargs):
        pass

    def _rest_endpoint(
        self,
        name: str,
        rule: str,
        method: str,
        serialization_handler: Optional["SerializationHandler"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        entrypoint = HTTPFoundationHandler(max_content_length=self.max_content_length)

        handler = entrypoint
        if authn_handler:
            handler = handler.wraps(authn_handler)
        elif self.authn_handler:
            handler = handler.wraps(self.authn_handler)

        if logging_handler:
            handler = handler.wraps(logging_handler)
        elif self.logging_handler:
            handler = handler.wraps(self.logging_handler)

        if tracing_handler:
            handler = handler.wraps(tracing_handler)
        elif self.tracing_handler:
            handler = handler.wraps(self.tracing_handler)

        if serialization_handler:
            handler = handler.wraps(serialization_handler)
        elif self.serialization_handler:
            handler = handler.wraps(self.serialization_handler)

        def wrapper(func):
            simple_handler = SimpleHandler(func=func)
            handler.wraps(simple_handler)
            endpoint = HTTPEndpoint(
                name=name,
                rule=rule,
                method=method,
                entrypoint=entrypoint,
                extras=extras,
            )
            self.add_endpoint(endpoint, **options)
            return func

        return wrapper

    def create(
        self,
        name: str,
        rule: str,
        data_cls: "ModelMetaCls",
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.POST,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_create_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.create(*args, **kwargs)(func)

    def get(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.GET,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_get_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.get(*args, **kwargs)(func)

    def update(
        self,
        name: str,
        rule: str,
        data_cls: "ModelMetaCls",
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.PATCH,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_update_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.update(*args, **kwargs)(func)

    def delete(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.DELETE,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_delete_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.delete(*args, **kwargs)(func)

    def list(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.GET,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_list_endpoint(self, *args, func, **kwargs):
        """
        """
        return self.list(*args, **kwargs)(func)

    def custom(
        self,
        name: str,
        rule: str,
        verb: str,
        method: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        serialization_helper: "SerializationHelper" = JSONSerializationHelper,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        if rule.endswith("/"):
            rule = rule[:-1]
        rule = "{}:{}".format(rule, verb)

        if method not in HTTPMethods.supported_methods:
            raise ValueError(
                "{} is not a supported HTTP method ({}).".format(
                    method, HTTPMethods.supported_methods
                )
            )

        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_handler=serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=method,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_custom_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        self.custom(*args, **kwargs)(func)

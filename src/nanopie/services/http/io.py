"""This module includes the base classes (interfaces) for requests and responses
in HTTP services.
"""

from typing import Any, Callable, Dict, Optional, Union

from ..base import RPCEndpoint, RPCParsedRequest, RPCRequest, RPCResponse
from ...model import Model


class HTTPRequest(RPCRequest):
    """The class for HTTP requests."""

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
        url: Union[str, Callable],
        headers: Union[Dict, Callable],
        content_length: Union[int, Callable],
        mime_type: Union[str, Callable],
        query_args: Union[Dict, Callable],
        binary_data: Callable,
        text_data: Callable,
    ):
        """Initializes an HTTP request.

        Args:
            url (Union[str, Callable]): The URL of the request, or a callable
                to get the URL of the request.
            headers (Union[Dict, Callable]): The headers of the request, or
                a callable to get the headers of the request.
            content_length (Union[int, Callable]): The content length of the
                request, or a callable to get the content length of the
                request.
            mime_type (Union[str, Callable]): The mime type of the request,
                or a callable to get the mime type of the request.
            query_args (Union[Dict, Callable]): The query arguments in the URI
                of the request, or a callable to get the query arguments in
                the URI of the request.
            binary_data (Callable): A callable to get the binary data payload
                of the request.
            text_data (Callable): A callable to get the text data payload of
                the request.
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
        """A helper method that resolves the callable.

        Args:
            v (Any): A callable or a regular value.

        Returns:
            Any: The return value of the callable or the original input.
        """
        if callable(v):
            return v()
        else:
            return v

    @property
    def url(self) -> str:
        """Returns the URL of the request."""
        return self._helper(self._url)

    @property
    def headers(self) -> Dict:
        """Returns the headers of the request."""
        return self._helper(self._headers)

    @property
    def content_length(self) -> int:
        """Returns the content length of the request."""
        return self._helper(self._content_length)

    @property
    def mime_type(self) -> str:
        """Returns the mime type of the request."""
        return self._helper(self._mime_type)

    @property
    def query_args(self) -> Dict:
        """Returns the query arguments in the URI of the request."""
        return self._helper(self._query_args)

    @property
    def binary_data(self) -> bytes:
        """Returns the binary data payload of the request."""
        return self._helper(self._binary_data)

    @property
    def text_data(self) -> str:
        """Returns the text data payload of the request."""
        return self._helper(self._text_data)


class HTTPParsedRequest(RPCParsedRequest):
    """The class for parsed HTTP requests."""

    __slots__ = ("_headers", "_query_args", "_data")

    def __init__(
        self,
        headers: Optional["Model"] = None,
        query_args: Optional["Model"] = None,
        data: Optional["Model"] = None,
    ):
        """Initializes a parsed HTTP request.

        A parsed HTTP request includes the headers, query arguments, and
        payload of incoming request parsed in accordance with the data models
        specified with the receiving endpoint.

        Args:
            headers (Optional[Model]): The headers of the request.
            query_args (Optional[Model]): The query arguments of the request.
            data (Optional[Model]): The data payload of the request.
        """
        self._headers = headers
        self._query_args = query_args
        self._data = data

    @property
    def headers(self):
        """Returns the headers of the request."""
        if not self._headers:
            raise ValueError("This endpoint is not configured with a header model.")

        return self._headers

    @property
    def query_args(self):
        """Returns the query arguments in the URI of the request."""
        if not self._query_args:
            raise ValueError("This endpoint is not configured with a query args model.")

        return self._query_args

    @property
    def data(self):
        """Returns the data payload of the request."""
        if not self._data:
            raise ValueError("This endpoint is not configured with a data model.")

        return self._data


class HTTPResponse(RPCResponse):
    """The class for HTTP responses."""

    __slots__ = ("_status_code", "_headers", "_mime_type", "_data")

    def __init__(
        self,
        status_code: int = 200,
        headers: Optional[Union[Dict, "Model"]] = None,
        mime_type: Optional[str] = None,
        data: Optional[Union[str, bytes, "Model"]] = None,
    ):
        """Initializes an HTTP response.

        Args:
            status_code (int): The status code of the HTTP response.
            headers (Optional[Union[Dict, Model]]): The headers of the HTTP
                response.
            mime_type (Optional[str]): The mime type of the HTTP response.
            data (Optional[Union[str, bytes, Model]]): The payload of the
                HTTP response.
        """
        self._status_code = None
        self._headers = None
        self._mime_type = None
        self._data = None

        self.status_code = status_code
        self.headers = headers
        self.mime_type = mime_type
        self.data = data

    @property
    def status_code(self) -> int:
        """Returns the status code of the HTTP response."""
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int):
        """Sets the status code of the HTTP response."""
        if type(status_code) != int:
            raise RuntimeError("HTTP Response must have a status code of the int type.")
        self._status_code = status_code

    @property
    def headers(self) -> [Dict, "Model"]:
        """Returns the headers of the HTTP response."""
        return self._headers

    @headers.setter
    def headers(self, headers: Optional[Dict]):
        """Sets the headers of the HTTP response."""
        if headers == None:
            headers = {}

        if type(headers) != dict and not isinstance(headers, Model):
            raise RuntimeError("HTTP Response must have a Model or a dict as headers.")

        self._headers = headers

    @property
    def mime_type(self) -> str:
        """Returns the mime type of the HTTP response."""
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: Optional[str]):
        """Sets the mime type of the HTTP response."""
        if mime_type == None:
            mime_type = ""

        if type(mime_type) != str:
            raise RuntimeError("The mime type must be a str.")

        self._mime_type = mime_type

    @property
    def data(self) -> Optional[Union[str, bytes, "Model"]]:
        """Returns the data payload of the HTTP response."""
        return self._data

    @data.setter
    def data(self, data: Optional[Union[str, bytes, "Model"]]):
        """Sets the data payload of the HTTP response."""
        if (
            data != None
            and type(data) not in [str, bytes]
            and not isinstance(data, Model)
        ):
            raise RuntimeError(
                "HTTP Response must have a str, a bytes or a Model as data."
            )

        self._data = data

    @property
    def is_processed(self):
        """Returns True if the headers or data payload are not of the basic data types."""
        if type(self._headers) != dict or type(self._data) not in [str, bytes]:
            return False

        return True


class HTTPEndpoint(RPCEndpoint):
    """The class for HTTP endpoints."""

    def __init__(self, method: str, **kwargs):
        """Initializes an HTTP endpoint.

        Args:
            method (str): The HTTP method supported by the endpoint.
            **kwargs: Arbitrary keyword arguments.
        """
        self.method = method

        super().__init__(**kwargs)

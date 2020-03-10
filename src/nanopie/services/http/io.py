from typing import Any, Callable, Dict, Optional, Union

from ..base import RPCEndpoint, RPCParsedRequest, RPCRequest, RPCResponse

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
        url: Union[str, Callable],
        headers: Union[Dict, Callable],
        content_length: Union[int, Callable],
        mime_type: Union[str, Callable],
        query_args: Union[Dict, Callable],
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


class HTTPParsedRequest(RPCParsedRequest):
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
        headers: Optional[Union[Dict, "Model"]] = None,
        mime_type: Optional[str] = None,
        data: Optional[Union[str, bytes, "Model"]] = None,
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
    def data(self) -> Optional[Union[str, bytes]]:
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
    def data(self, data: Optional[Union[str, bytes]]):
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
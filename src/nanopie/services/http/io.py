from typing import Any, Callable, Dict, Optional, Union

from ..base import RPCEndpoint, RPCParsedRequest, RPCRequest, RPCResponse
from ...model import Model


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
        """
        """
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
    def headers(self) -> [Dict, "Model"]:
        """
        """
        return self._headers

    @headers.setter
    def headers(self, headers: Optional[Dict]):
        """
        """
        if headers == None:
            headers = {}

        if type(headers) != dict and not isinstance(headers, Model):
            raise RuntimeError(
                "HTTP Response must have a Model or a dict " "as headers."
            )

        self._headers = headers

    @property
    def mime_type(self) -> str:
        """
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type: Optional[str]):
        """
        """
        if mime_type == None:
            mime_type = ""

        if type(mime_type) != str:
            raise RuntimeError("The mime type must be a str.")

        self._mime_type = mime_type

    @property
    def data(self) -> Optional[Union[str, bytes, "Model"]]:
        """
        """
        return self._data

    @data.setter
    def data(self, data: Optional[Union[str, bytes, "Model"]]):
        """
        """
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
        """
        """
        if type(self._headers) != dict or type(self._data) not in [str, bytes]:
            return False

        return True


class HTTPEndpoint(RPCEndpoint):
    """
    """

    def __init__(self, method: str, **kwargs):
        """
        """
        self.method = method

        super().__init__(**kwargs)

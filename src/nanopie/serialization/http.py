from typing import Optional

from .base import SerializationHandler
from ..globals import request, svc_ctx
from ..misc import format_error_message
from ..misc.errors import SerializationError
from ..model import Model
from ..services.http.io import HTTPParsedRequest, HTTPResponse

INVALID_MIME_TYPE_RESPONSE = HTTPResponse(
    status_code=400,
    headers={},
    mime_type="text/html",
    data=("<h2>400 Bad Request: invalid mime type.</h2>"),
)
INVALID_HEADERS_RESPONSE = HTTPResponse(
    status_code=400,
    headers={},
    mime_type="text/html",
    data=("<h2>400 Bad Request: invalid headers.</h2>"),
)
INVALID_QUERY_ARGS_RESPONSE = HTTPResponse(
    status_code=400,
    headers={},
    mime_type="text/html",
    data=("<h2>400 Bad Request: invalid URI query arguments.</h2>"),
)
INVALID_DATA_RESPONSE = HTTPResponse(
    status_code=400,
    headers={},
    mime_type="text/html",
    data=("<h2>400 Bad Request: invalid body data.</h2>"),
)


class HTTPSerializationHandler(SerializationHandler):
    """
    """

    def __init__(
        self,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        data_cls: Optional["ModelMetaCls"] = None,
        **kwargs
    ):
        """
        """
        self._headers_cls = headers_cls
        self._query_args_cls = query_args_cls
        self._data_cls = data_cls

        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        """
        """
        helper = self._serialization_helper

        try:
            mime_type = getattr(request, "mime_type")
            headers_dikt = getattr(request, "headers")
            query_args_dikt = getattr(request, "query_args")
            if self._serialization_helper.binary:
                raw_data = getattr(request, "binary_data")
            else:
                raw_data = getattr(request, "text_data")
        except AttributeError:
            raise AttributeError("The incoming request is not a valid HTTP " "request.")

        if mime_type.lower() != helper.mime_type.lower():
            message = "The incoming request does not have the expected " "mime type."
            message = format_error_message(
                message=message,
                provided_mime_type=mime_type,
                expected_mime_type=helper.mime_type,
            )
            raise SerializationError(message, response=INVALID_MIME_TYPE_RESPONSE)

        headers = None
        if self._headers_cls:
            try:
                headers = self._headers_cls.from_dikt(headers_dikt, altchar='-')
            except Exception as ex:
                message = (
                    "The incoming request does not have " "valid headers ({})."
                ).format(str(ex))
                raise SerializationError(message, response=INVALID_HEADERS_RESPONSE)

        query_args = None
        if self._query_args_cls:
            try:
                query_args = self._query_args_cls.from_dikt(query_args_dikt)
            except Exception as ex:
                message = (
                    "The incoming request does not have "
                    "valid URI query arguments ({})."
                ).format(str(ex))
                raise SerializationError(message, response=INVALID_QUERY_ARGS_RESPONSE)

        data = None
        if self._data_cls:
            try:
                data = self._data_cls.from_dikt(helper.from_data(data=raw_data))
            except Exception as ex:
                message = (
                    "The incoming request does not have " "valid body data ({})."
                ).format(str(ex))
                raise SerializationError(message, response=INVALID_DATA_RESPONSE)

        parsed_request = HTTPParsedRequest(
            headers=headers, query_args=query_args, data=data
        )
        svc_ctx["parsed_request"] = parsed_request

        res = super().__call__(*args, **kwargs)

        if isinstance(res, HTTPResponse):
            if isinstance(res.headers, Model):
                try:
                    res.headers = res.headers.to_dikt()
                except Exception as ex:
                    message = (
                        "Cannot serialize the headers in the response. " "({})"
                    ).format(str(ex))
                    raise SerializationError(message)
            if isinstance(res.data, Model):
                res.mime_type = helper.mime_type
                try:
                    res.data = helper.to_data(res.data.to_dikt())
                except Exception as ex:
                    message = (
                        "Cannot serialize the data in the response. " "({})"
                    ).format(str(ex))
                    raise SerializationError(message)

        return res

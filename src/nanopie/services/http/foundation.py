from typing import Optional

from ...globals import request
from ...handler import Handler
from ...misc import format_error_message
from ...misc.errors import FoundationError
from .io import HTTPResponse

REQUEST_TOO_LARGE_RESPONSE = HTTPResponse(
    status_code=400,
    headers={},
    mime_type="text/html",
    data="<h2>400 Bad Request: request is too large.</h2>",
)


class HTTPFoundationHandler(Handler):
    """
    """

    def __init__(self, max_content_length: Optional[int] = 6000):
        """
        """
        self._max_content_length = max_content_length

        super().__init__()

    def __call__(self, *args, **kwargs):
        """
        """
        try:
            content_length = getattr(request, "content_length")
        except AttributeError:
            raise RuntimeError("The incoming request is not a valid HTTP " "request.")

        if content_length and content_length >= self._max_content_length:
            message = "Request is too large."
            message = format_error_message(message, provided_size=content_length)
            raise FoundationError(message, response=REQUEST_TOO_LARGE_RESPONSE)

        return self.wrapped(*args, **kwargs)

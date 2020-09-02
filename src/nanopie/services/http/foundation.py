"""This module includes the foundation handler for HTTP services.

Foundation handlers server as entrypoint for handler chains in all endpoints.
It performs a number of basic functionalities, such as checking the
content length of the request, and pass the baton to other chained handlers.
"""

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
    """The foundation handler for HTTP services."""

    def __init__(self, max_content_length: Optional[int] = 6000):
        """Initializes an HTTP foundation handler.

        Args:
            max_content_length (int, Optional): The maximum content length of
                the request.
        """
        self._max_content_length = max_content_length

        super().__init__()

    def __call__(self, *args, **kwargs):
        """Runs the foundation handler.

         Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary named arguments.

        Returns:
            Any: Any object.
        """
        try:
            content_length = getattr(request, "content_length")
        except AttributeError:
            raise RuntimeError("The incoming request is not a valid HTTP " "request.")

        if content_length and content_length >= self._max_content_length:
            message = "Request is too large."
            message = format_error_message(message, provided_size=content_length)
            raise FoundationError(message, response=REQUEST_TOO_LARGE_RESPONSE)

        return super().__call__(*args, **kwargs)

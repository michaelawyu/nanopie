"""This module includes the handler for HTTP API key authentication.
"""

from .base import CredentialExtractor, AuthenticationHandler
from .creds.key import Key
from ..misc.errors import AuthenticationError
from ..services.http.io import HTTPResponse

INVALID_HEADER_RESPONSE = HTTPResponse(
    status_code=401,
    headers={},
    mime_type="text/html",
    data=("<h2>401 Unauthorized: Must include an API key in the request header.</h2>"),
)
INVALID_QUERY_ARGS_RESPONSE = HTTPResponse(
    status_code=401,
    headers={},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: Must include an API key in the URI query string.</h2>"
    ),
)
INVALID_KEY_RESPONSE = HTTPResponse(
    status_code=403,
    headers={},
    mime_type="text/html",
    data=("<h2>403 Forbidden: The provided API key is not valid.</h2>"),
)


class HTTPAPIKeyModes:
    """The modes which HTTP API key authentication uses.

    HTTP API keys usually reside in two places, the headers of the HTTP
    request (HEADER mode), or the query parameters in the URI (URI_QUERY mode).
    """

    HEADER = "HEADER"
    URI_QUERY = "URI_QUERY"
    supported_modes = [HEADER, URI_QUERY]


class HTTPAPIKeyExtractor(CredentialExtractor):
    """The credential extractor for HTTP API key authentication."""

    def __init__(self, mode: str, key_field_name: str):
        """Initializes a credential extractor.

        Args:
            mode (str): The mode this credential extractor will use. It
                determines where the API key resides. There are two modes:
                HEADER and URI_QUERY; see also the class `HTTPAPIKeyModes`.
            key_field_name (str): The name of the header or the query
                parameter that contains the API key.
        """
        if mode not in HTTPAPIKeyModes.supported_modes:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    HTTPAPIKeyModes.supported_modes
                )
            )
        self.mode = mode
        self.key_field_name = key_field_name

    def extract(self, request: "HTTPRequest") -> "Key":
        """Extracts a key credential from an HTTP request.

        Args:
            request (HTTPRequest): An HTTP request.

        Returns:
            Key: The extracted HTTP API key credential.
        """
        if self.mode == HTTPAPIKeyModes.HEADER:
            try:
                headers = getattr(request, "headers")
            except AttributeError:
                raise AttributeError(
                    "The incoming request is not a valid " "HTTP request."
                )

            auth_header = None
            for k in headers:
                if k.lower() == self.key_field_name.lower():
                    auth_header = headers[k]

            if not auth_header:
                message = (
                    "The incoming request does not have an API key in "
                    "the request header."
                )
                raise AuthenticationError(message, response=INVALID_HEADER_RESPONSE)
            key = auth_header
        elif self.mode == HTTPAPIKeyModes.URI_QUERY:
            try:
                query_args = getattr(request, "query_args")
            except AttributeError:
                raise AttributeError(
                    "The incoming request is not a valid " "HTTP request."
                )

            key = query_args.get(self.key_field_name)
            if not key:
                message = (
                    "The incoming request does not have an API key "
                    "in the query string."
                )
                raise AuthenticationError(message, response=INVALID_QUERY_ARGS_RESPONSE)
        else:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    HTTPAPIKeyModes.supported_modes
                )
            )

        credential = Key(key=key)
        return credential


class HTTPAPIKeyAuthenticationHandler(AuthenticationHandler):
    """The authentication handler for HTTP API key authentication."""

    def __init__(
        self,
        mode: str,
        key_field_name: str,
        credential_validator: "CredentialValidator",
    ):
        """Initializes an HTTP API key authentication handler.

        Args:
            mode (str): The mode this authentication handler will use. It
                determines where the API key resides. There are two modes:
                HEADER and URI_QUERY; see also the class `HTTPAPIKeyModes`.
            key_field_name (str): The name of the header or the query
                parameter that contains the API key.
            credential_validator (CredentialValidator): A credential
                validator. To prepare a credential validator dynamically at
                runtime, see the method `before_authentication`.
        """
        credential_extractor = HTTPAPIKeyExtractor(
            mode=mode, key_field_name=key_field_name
        )
        super().__init__(
            credential_extractor=credential_extractor,
            credential_validator=credential_validator,
        )

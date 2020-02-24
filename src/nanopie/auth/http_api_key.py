from .base import CredentialExtractor, AuthenticationHandler
from .creds.key import Key
from ..misc.errors import AuthenticationError
from ..services.http.base import HTTPResponse

INVALID_HEADER_RESPONSE = HTTPResponse(
    status_code=401,
    headers={},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: must include an API key in the " "request header.</h2>"
    ),
)
INVALID_QUERY_ARGS_RESPONSE = HTTPResponse(
    status_code=401,
    headers={},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: must include an API key " "in the URI query string.</h2>"
    ),
)
INVALID_TOKEN_RESPONSE = HTTPResponse(
    status_code=403,
    headers={},
    mime_type="text/html",
    data=("<h2>403 Forbidden: the provided API key is not valid " "</h2>"),
)


class HTTPAPIKeyModes:
    """
    """

    HEADER = "HEADER"
    URI_QUERY = "URI_QUERY"
    supported_modes = [HEADER, URI_QUERY]


class HTTPAPIKeyExtractor(CredentialExtractor):
    """
    """

    def __init__(self, mode: str, key_field_name: str):
        """
        """
        if mode not in HTTPAPIKeyModes.supported_modes:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    HTTPAPIKeyModes.supported_modes
                )
            )
        self.mode = mode
        self.key_field_name = key_field_name

    def extract(self, request: "HTTPRequest"):
        """
        """
        if self.mode == HTTPAPIKeyModes.HEADER:
            headers = getattr(request, "headers")
            if not headers:
                raise RuntimeError(
                    "The incoming request is not a valid HTTP " "request."
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
            query_args = getattr(request, "query_args")
            if not query_args:
                raise RuntimeError(
                    "The incoming request is not a valid HTTP " "request."
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
    """
    """

    def __init__(
        self,
        mode: str,
        key_field_name: str,
        credential_validator: "CredentialValidator",
    ):
        """
        """
        credential_extractor = HTTPAPIKeyExtractor(
            mode=mode, key_field_name=key_field_name
        )
        super().__init__(
            credential_extractor=credential_extractor,
            credential_validator=credential_validator,
        )

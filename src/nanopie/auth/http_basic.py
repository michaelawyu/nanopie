import base64

from .base import CredentialExtractor, AuthenticationHandler
from .creds.user_credential import UserCredential
from ..misc.errors import AuthenticationError
from ..services.http.base import HTTPResponse

INVALID_HEADER_RESPONSE = HTTPResponse(
    status_code=401,
    headers={"WWW-Authenticate": "Basic"},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: must include an HTTP Authorization "
        "request header of the Basic type.</h2>"
    ),
)
INVALID_CREDENTIAL_RESPONSE = HTTPResponse(
    status_code=403,
    headers={"WWW-Authenticate": "Basic"},
    mime_type="text/html",
    data=("<h2>403 Forbidden: the provided user credential is not valid " "</h2>"),
)


class HTTPBasicUserCredentialExtractor(CredentialExtractor):
    """
    """

    def extract(self, request: "HTTPRequest"):
        """
        """
        headers = getattr(request, "headers")
        if not headers:
            raise RuntimeError("The incoming request is not a valid HTTP " "request.")

        auth_header = None
        for k in headers:
            if k.lower() == "authorization":
                auth_header = headers[k]

        if not auth_header:
            message = (
                "The incoming request does not have an HTTP "
                "Authorization request header."
            )
            raise AuthenticationError(message, response=INVALID_HEADER_RESPONSE)
        if not auth_header.startswith("Basic "):
            message = (
                "The incoming request does not have an HTTP "
                "Authorization request header with the Basic type."
            )
            raise AuthenticationError(message, response=INVALID_HEADER_RESPONSE)

        data = auth_header[6:]
        try:
            decoded_data = base64.b64decode(data)
        except Exception as ex:
            message = "Cannot decode the credential data ({}).".format(str(ex))
            raise AuthenticationError(message, response=INVALID_CREDENTIAL_RESPONSE)
        t = decoded_data.split(":")
        if len(t >= 2):
            username = t[0]
            password = "".join(t[1:])
        else:
            message = "Provided user credential ({}) is malformed.".format(t)
            raise AuthenticationError(message, response=INVALID_CREDENTIAL_RESPONSE)

        credential = UserCredential(username=username, password=password)
        return credential


class HTTPBasicAuthenticationHandler(AuthenticationHandler):
    """
    """

    def __init__(self, credential_validator: "CredentialValidator"):
        """
        """
        credential_extractor = HTTPBasicUserCredentialExtractor()
        super().__init__(
            credential_extractor=credential_extractor,
            credential_validator=credential_validator,
        )

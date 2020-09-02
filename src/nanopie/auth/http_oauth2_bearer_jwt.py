"""This module includes the handler for HTTP OAuth2 Bearer w/ JWT authentication.

See also RFC 6750, RFC 7519.
"""

from typing import Optional

from .base import CredentialExtractor, AuthenticationHandler
from .creds.jwt import JWT, JWTValidator
from ..misc.errors import AuthenticationError
from ..services.http.io import HTTPResponse

INVALID_HEADER_RESPONSE = HTTPResponse(
    status_code=401,
    headers={"WWW-Authenticate": "Bearer"},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: Must include an HTTP Authorization "
        "request header of the Bearer type.</h2>"
    ),
)
INVALID_QUERY_ARGS_RESPONSE = HTTPResponse(
    status_code=401,
    headers={"WWW-Authenticate": "Bearer"},
    mime_type="text/html",
    data=(
        "<h2>401 Unauthorized: Must include an access_token argument "
        "in the URI query string.</h2>"
    ),
)
INVALID_TOKEN_RESPONSE = HTTPResponse(
    status_code=403,
    headers={"WWW-Authenticate": "Bearer error=invalid_token"},
    mime_type="text/html",
    data=("<h2>403 Forbidden: The provided access token is not valid " "</h2>"),
)


class HTTPOAuth2BearerJWTModes:
    """The modes which HTTP OAuth2 Bearer authentication uses.

    RFC 6750 specifies three places where access tokens may reside. At this
    moment two places are supported: the headers of the HTTP request
    (HEADER mode), or the query parameters in the URI (URI_QUERY mode).
    """

    HEADER = "HEADER"
    URI_QUERY = "URI_QUERY"
    supported_modes = [HEADER, URI_QUERY]


class HTTPOAuth2BearerJWTExtractor(CredentialExtractor):
    """The credential extractor for HTTP OAuth2 Bearer w/ JWT authentication."""

    def __init__(self, mode: str):
        """"""
        if mode not in HTTPOAuth2BearerJWTModes.supported_modes:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    HTTPOAuth2BearerJWTModes.supported_modes
                )
            )
        self.mode = mode

    def extract(self, request: "HTTPRequest") -> "JWT":
        """Extracts a JWT credential from an HTTP request.

        Args:
            request (HTTPRequest): An HTTP request.

        Returns:
            JWT: A JWT credential.
        """
        if self.mode == HTTPOAuth2BearerJWTModes.HEADER:
            try:
                headers = getattr(request, "headers")
            except AttributeError:
                raise AttributeError(
                    "The incoming request is not a valid HTTP " "request."
                )

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
            if not auth_header.startswith("Bearer "):
                message = (
                    "The incoming request does not have an HTTP "
                    "Authorization request header with the Bearer type."
                )
                raise AuthenticationError(message, response=INVALID_HEADER_RESPONSE)
            token = auth_header[7:]
        elif self.mode == HTTPOAuth2BearerJWTModes.URI_QUERY:
            try:
                query_args = getattr(request, "query_args")
            except AttributeError:
                raise AttributeError(
                    "The incoming request is not a valid " "HTTP request."
                )

            token = query_args.get("access_token")
            if not token:
                message = (
                    "The incoming request does not have an "
                    "access_token argument in the query string."
                )
                raise AuthenticationError(message, response=INVALID_QUERY_ARGS_RESPONSE)
        else:
            raise ValueError(
                "mode must be one of the following values: {}".format(
                    HTTPOAuth2BearerJWTModes.supported_modes
                )
            )

        try:
            credential = JWT(token=token)
        except AuthenticationError as ex:
            ex.response = INVALID_TOKEN_RESPONSE
            raise ex
        return credential


class HTTPOAuth2BearerJWTValidator(JWTValidator):
    """The credential validator for HTTP OAuth2 Bearer w/ JWT authentication.

    See also `JWTValidator`.
    """

    def validate(self, credential):
        """"""
        try:
            super().validate(credential)
        except AuthenticationError as ex:
            ex.response = INVALID_TOKEN_RESPONSE
            raise ex


class HTTPOAuth2BearerJWTAuthenticationHandler(AuthenticationHandler):
    """The authentication handler for HTTP OAuth2 Bearer w/ JWT authentication."""

    def __init__(
        self,
        key_or_secret: str,
        algorithm: str,
        mode: Optional[str] = HTTPOAuth2BearerJWTModes.HEADER,
        use_pycrypto: bool = False,
        use_ecdsa: bool = False,
        **kwargs
    ):
        """Initializes an HTTP OAuth2 Bearer w/ JWT authentication handler.

        Args:
            key_or_secret (str): The public key (if using asymmetric encryption,
                e.g. ES/RS/PS algorithms) or secret (if using symmetric
                encryption, e.g. HS algorithm) for decrypting JWTs.
            algorithm (str): The encryption algorithm for encrypting/decrypting
                JWTs. It must be one of the followings values:
                - HS256, HS384, or HS512 (HMAC with SHA-256/SHA-384/SHA-512)
                - RS256, RS384, or RS512 (RSA with SHA-256/SHA-384/SHA-512)
                - ES256, ES384, or ES512 (ECDSA with SHA-256/SHA-384/SHA-512)
                - PS256, PS384, or PS512 (PSS with SHA-256/SHA-384/SHA-512)
            use_pycrypto (bool): If set to True, use the pycrypto package for
                encryption/decryption instead of the default cryptography
                package. This package only supports RS algorithms.
            use_ecdsa (bool): If set to True, use the ecdsa package for
                encryption/decryption instead of the default cryptography
                package. This package only supports ES algorithms.
            **kwargs: Other validation options. Available options are:
                - verify_signature (bool): If set to False, the JWT signature
                  will not be validated. Defaults to True.
                - verify_exp (bool): If set to False, the exp (expiration)
                  claim of the JWT (if any) will not be validated. Defaults
                  to True.
                - verify_nbf (bool): If set to False, the nbf (not before)
                  claim of the JWT (if any) will not be validated. Defaults
                  to True.
                - verify_iat (bool): If set to False, the iat (issued at)
                  claim of the JWT (if any) will not be validated. Defaults
                  to True.
                - verify_aud (bool): If set to True, the aud (audience)
                  claim of the JWT will be validated. Defaults to False.
                - verify_iss (bool): If set to True, the iss (issuer)
                  claim of the JWT will be validated. Defaults to False.
                - require_exp (bool): If set to True, the exp (expiration)
                  claim must be present in the JWT. Defaults to False.
                - require_iat (bool): If set to True, the iat (issued at)
                  claim must be present in the JWT. Defaults to False.
                - require_nbf (bool): If set to True, the nbf (not before)
                  claim must be present in the JWT. Defaults to False.
                - audience (str, Optional): The expected audience of the JWT.
                - issuer (str, Optional): The expected issuer of the JWT.
                - leeway (int): The margin of error for the exp (expiration)
                  claim. Defaults to 0.
                See also pyjwt API reference
                (https://pyjwt.readthedocs.io/en/latest/api.html#jwt.decode).
        """
        self.algorithm = algorithm
        self.key_or_secret = key_or_secret
        self.kwargs = kwargs

        credential_extractor = HTTPOAuth2BearerJWTExtractor(mode=mode)
        credential_validator = HTTPOAuth2BearerJWTValidator(
            key_or_secret=key_or_secret,
            algorithm=algorithm,
            use_pycrypto=use_pycrypto,
            use_ecdsa=use_ecdsa,
            **kwargs
        )
        super().__init__(
            credential_extractor=credential_extractor,
            credential_validator=credential_validator,
        )

from typing import Optional

from .base import CredentialExtractor, AuthenticationHandler
from .creds.jwt import JWT, JWTValidator
from ..globals import request
from ..misc.errors import AuthenticationError
from ..services.http.base import HTTPResponse

INVALID_HEADER_RESPONSE = HTTPResponse(
    status_code=401,
    headers={
        'WWW-Authenticate': 'Bearer'
    },
    mime_type='text/html',
    text_data=('<h2>401 Unauthorized: must include an HTTP Authorization '
               'request header of the Bearer type.</h2>')
)
INVALID_QUERY_ARGS_RESPONSE = HTTPResponse(
    status_code=401,
    headers={
        'WWW-Authenticate': 'Bearer'
    },
    mime_type='text/html',
    text_data=('<h2>401 Unauthorized: must include an access_token argument '
               'in the URI query string.</h2>')
)
INVALID_TOKEN_RESPONSE = HTTPResponse(
    status_code=403,
    headers={
        'WWW-Authenticate': 'Bearer error=invalid_token'
    },
    mime_type='text/html',
    text_data=('<h2>403 Forbidden: the provided access token is not valid '
               '</h2>')
)

class HTTPOAuth2BearerJWTModes:
    """
    """
    HEADER = 'HEADER'
    URI_QUERY = 'URI_QUERY'
    supported_modes = [ HEADER, URI_QUERY ]

class HTTPOAuth2BearerJWTExtractor(CredentialExtractor):
    """
    """
    def __init__(self, mode: str):
        """
        """
        if mode not in HTTPOAuth2BearerJWTModes.supported_modes:
            raise ValueError(
                'mode must be one of the following values: {}'.format(
                    HTTPOAuth2BearerJWTModes.supported_modes))
        self.mode = mode
    
    def extract(self, request: 'HTTPRequest'):
        """
        """
        if self.mode == HTTPOAuth2BearerJWTModes.HEADER:
            headers = getattr(request, 'headers')
            if not headers:
                raise RuntimeError('The incoming request is not a valid HTTP '
                                   'request.')

            auth_header = None
            for k in headers:
                if k.lower() == 'authorization':
                    auth_header = headers[k]
            
            if not auth_header:
                message = ('The incoming request does not have an HTTP '
                           'Authorization request header.')
                raise AuthenticationError(message,
                                          response=INVALID_HEADER_RESPONSE)
            if not auth_header.startswith('Bearer '):
                message = ('The incoming request does not have an HTTP '
                           'Authorization request header with the Bearer type.')
                raise AuthenticationError(message,
                                          response=INVALID_HEADER_RESPONSE)
            token = auth_header[7:]
        elif self.mode == HTTPOAuth2BearerJWTModes.URI_QUERY:
            query_args = getattr(request, 'query_args')
            if not query_args:
                raise RuntimeError('The incoming request is not a valid HTTP '
                                   'request.')
            
            token = query_args.get('access_token')
            if not token:
                message = ('The incoming request does not have an '
                           'access_token argument in the query string.')
                raise AuthenticationError(message,
                                          response=INVALID_QUERY_ARGS_RESPONSE)
        else:
            raise ValueError(
                'mode must be one of the following values: {}'.format(
                    HTTPOAuth2BearerJWTModes.supported_modes))
        
        try:
            credential = JWT(token=token)
        except AuthenticationError as ex:
            ex.response = INVALID_TOKEN_RESPONSE
            raise ex
        return credential

class HTTPOAuth2BearerJWTValidator(JWTValidator):
    """
    """
    def validate(self, credential):
        """
        """
        try:
            super().validate(credential)
        except AuthenticationError as ex:
            ex.response = INVALID_TOKEN_RESPONSE
            raise ex

class HTTPOAuth2BearerJWTAuthenticationHandler(AuthenticationHandler):
    """
    """
    def __init__(self,
                 key_or_secret: str,
                 algorithm: str,
                 mode: Optional[str] = HTTPOAuth2BearerJWTModes.HEADER,
                 use_pycrypto: bool = False,
                 use_ecdsa: bool = False):
        """
        """
        credential_extractor = HTTPOAuth2BearerJWTExtractor(mode=mode)
        credential_validator = HTTPOAuth2BearerJWTValidator(
            key_or_secret=key_or_secret,
            algorithm=algorithm,
            use_pycrypto=use_pycrypto,
            use_ecdsa=use_ecdsa
        )
        super().__init__(credential_extractor=credential_extractor,
                         credential_validator=credential_validator)

from typing import Optional

from .base import AuthenticationError

class HTTPOAuth2BearerHeaderMissingError(AuthenticationError):
    """
    """
    _message = ('Unauthorized request: '
                'OAuth2 Bearer request header is not found.')

    def __init__(self, message=None):
        """
        """
        self._http_status_code = 401
        self._extra_headers = { 'WWW-Authenticate': 'Bearer' }
        self._body_text = ('<h2>401: Unauthorized '
                           '(OAuth2 Bearer/Request Header Not Found)')
        super().__init__(message=self.get_message(message))

class HTTPOAuth2BearerQueryArgMissingError(AuthenticationError):
    """
    """
    _message = ('Unauthorized request: '
                'OAuth2 Bearer URI query param is not found.')

    def __init__(self, message=None):
        """
        """
        self._http_status_code = 401
        self._extra_headers = { 'WWW-Authenticate': 'Bearer' }
        self._body_text = ('<h2>401: Unauthorized '
                           '(OAuth2 Bearer/URI Query Param Not Found)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPOAuth2BearerTokenNotFoundError(AuthenticationError):
    """
    """
    _message = ('Unauthorized request: '
                'OAuth2 Bearer token is not found.')

    def __init__(self,
                 message: Optional[str] = None):
        """
        """
        self._http_status_code = 401
        self._extra_headers = { 'WWW-Authenticate': 'Bearer' }
        self._body_text = ('<h2>401: Unauthorized '
                           '(OAuth2 Bearer/Token Not Found)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPOAuth2BearerTokenInvalidError(AuthenticationError):
    """
    """
    _message = ('Forbidden: '
                'OAuth2 Bearer token is invalid.')

    def __init__(self,
                 message: Optional[str] = None):
        """
        """
        self._extra_headers = {
            'WWW-Authenticate': 'Bearer error=invalid_token'
        }
        self._body_text = ('<h2>403: Forbidden '
                           '(OAuth2 Bearer/Invalid Token)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPBasicAuthHeaderMissingError(AuthenticationError):
    """
    """
    _message = ('Unauthorized request: '
                'HTTP Basic Auth header is not found.')

    def __init__(self, message: Optional[str] = None):
        """
        """
        self._http_status_code = 401
        self._extra_headers = { 'WWW-Authenticate': 'Basic' }
        self._body_text = ('<h2>401: Unauthorized '
                           '(HTTP Basic Auth/Request Header Not Found)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPBasicAuthUserCredentialInvalidError(AuthenticationError):
    """
    """
    _message = ('Forbidden: '
                'User credential is invalid.')

    def __init__(self, message=None):
        self._http_status_code = 403
        self._extra_headers = { 'WWW-Authenticate': 'Basic' }
        self._body_text = ('<h2>403: Forbidden '
                           '(HTTP Basic Auth/User Credential Invalid)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPAPIKeyAuthHeaderMissingError(AuthenticationError):
    """
    """
    _message = ('Unauthorized: '
                'API Key request header is not found.')

    def __init__(self, param_name: str, message: Optional[str] = None):
        """
        """
        self._http_status_code = 401
        self._body_text = ('<h2>401: Unauthorized '
                           '(API Key Not Found in Request Header)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPAPIKeyAuthQueryArgMissingError(AuthenticationError):
    """
    """
    _message = ('Unauthorized: '
                'API Key URI query param is not found.')

    def __init__(self, param_name: str, message: Optional[str] = None):
        """
        """
        self._http_status_code = 401
        self._body_text = ('<h2>401: Unauthorized '
                           '(API Key Not Found in URI Query Param)</h2>')
        super().__init__(message=self.get_message(message))

class HTTPAPIKeyInvalidError(AuthenticationError):
    """
    """
    _message = ('Forbidden: '
                'API Key is invalid.')

    def __init__(self, param_name: str, message: Optional[str] = None):
        """
        """
        self._http_status_code = 403
        self._body_text = ('<h2>403: Forbidden '
                           '(API Key Invalid)</h2>')
        super().__init__(message=self.get_message(message))

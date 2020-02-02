from .base import HTTPAuthenticationError

class HTTPOAuth2BearerHeaderMissingError(HTTPAuthenticationError):
    """
    """
    def __init__(self, message=None):
        """
        """
        http_status_code = 400
        headers = {
            'WWW-Authenticate': 'Bearer'
        }
        body_text = ('Authorization Header for HTTP OAuth2 Bearer Token '
                     'Authentication is missing or malformed in the request.')
        if not message:
            message = body_text
        super().__init__(http_status_code=http_status_code,
                         headers=headers,
                         message=message)

class HTTPOAuth2BearerQueryArgMissingError(HTTPAuthenticationError):
    """
    """
    def __init__(self, message=None):
        """
        """
        http_status_code = 400
        headers = {
            'WWW-Authenticate': 'Bearer'
        }
        body_text = ('access_token query argument for HTTP OAuth2 Bearer Token '
                     'Authentication is missing or malformed in the request.')
        if not message:
            message = body_text
        super().__init__(http_status_code, headers, message=message)

class HTTPOAuth2BearerTokenNotFoundError(HTTPAuthenticationError):
    """
    """
    def __init__(self,
                 message: Optional[str] = None):
        """
        """
        http_status_code = 400
        headers = {
            'WWW-Authenticate': 'Bearer'
        }
        body_text = ('Token is not found.')
        if not message:
            message = body_text
        super().__init__(http_status_code=http_status_code,
                         headers=headers,
                         body_text=body_text
                         message=message)

class HTTPOAuth2BearerTokenInvalidError(HTTPAuthenticationError):
    """
    """
    def __init__(self,
                 wrapped: 'CredentialError',
                 message: Optional[str] = None):
        """
        """
        self.wrapped = wrapped
        http_status_code = 401
        headers = {
            'WWW-Authenticate': 'Bearer error=invalid_token'
        }
        body_text = ('Token is not valid.')
        if not message:
            message = str(wrapped)
        super().__init__(http_status_code=http_status_code,
                         headers=headers,
                         body_text=body_text
                         message=message)

class HTTPBasicAuthHeaderMissingError(HTTPAuthenticationError):
    """
    """
    def __init__(self, message: Optional[str] = None):
        """
        """
        http_status_code = 400
        headers = {
            'WWW-Authenticate': 'Basic'
        }
        body_text = ('Authorization Header for HTTP Basic Authentication '
                     'is missing or malformed in the request.')
        if not message:
            message = body_text
        super().__init__(http_status_code=http_status_code,
                         headers=headers,
                         body_text=body_text,
                         message=message)

class HTTPBasicAuthUserCredentialInvalidError(HTTPAuthenticationError):
    """
    """
    def __init__(self, message=None):
        http_status_code = 401
        headers = {
            'WWW-Authenticate': 'Basic'
        }
        body_text = ('User credential is not valid.')
        if not message:
            message = body_text
        super().__init__(http_status_code = http_status_code,
                         headers=headers,
                         body_text=body_text,
                         message=message)

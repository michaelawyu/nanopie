from ..base import Authenticator

try:
    import pyjwt
except ImportError:
    raise NotImplementedError

class OAuth2BearerJWTAuthenticator(Authenticator):
    """
    """
    def __init__(self):
        raise NotImplementedError

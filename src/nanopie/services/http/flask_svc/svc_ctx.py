from ..base import ServiceContext

class FlaskServiceContext(ServiceContext):
    """
    """
    __slots__ = ('_svc', '_api_params', '_auth_ctx')

    def __init__(self, svc: 'HTTPService'):
        """
        """
        self._svc = svc
        self._api_params = None
        self._auth_ctx = None

    @property
    def svc(self):
        """
        """
        return self._svc
    
    @svc.setter
    def svc(self, svc: 'HTTPService'):
        """
        """
        self._svc = svc
    
    @property
    def api_params(self):
        """
        """
        return self._api_params
    
    @api_params.setter
    def api_params(self, api_params: 'APIParams'):
        """
        """
        self._api_params = api_params
    
    @property
    def auth_ctx(self):
        """
        """
        return self.auth_ctx
    
    @auth_ctx.setter
    def auth_ctx(self, auth_ctx: 'AuthContext'):
        """
        """
        self._auth_ctx = auth_ctx

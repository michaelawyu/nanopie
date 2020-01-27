from ..base import ServiceContext

class FlaskServiceContext(ServiceContext):
    """
    """
    __slots__ = ('_svc', '_api_params')

    def __init__(self, svc: 'HTTPService', api_params: 'APIParams'):
        """
        """
        self._svc = svc
        self._api_params = api_params
    
    @property
    def svc(self) -> 'HTTPService':
        """
        """
        return self._svc
    
    @property
    def api_params(self) -> 'APIParams':
        """
        """
        return self._api_params

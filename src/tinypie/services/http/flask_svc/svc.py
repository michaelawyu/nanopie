from functools import partial
from typing import Callable, Dict, List, Optional

try:
    import flask
except ImportError:
    raise ImportError(
        'The Flask (https://pypi.org/projectx/Flask/) package is required to '
        'set up a Flask service. To install this package, run'
        '`pip install Flask`.'
    )

from ....auth.base import AuthContext
from .api_params import FlaskAPIParams
from ..base import HTTPService
from ..globals import svc_ctx, look_up_attr
from ..methods import HTTPMethods
from ....misc.errors import HTTPAuthenticationError
from ....serializers import JSONSerializer
from .svc_ctx import FlaskServiceContext

class FlaskService(HTTPService):
    """
    """
    def __init__(self,
                 app: flask.Flask,
                 serializer: 'Serializer' = JSONSerializer(),
                 authenticator: 'HTTPAuthenticator' = None,
                 max_content_length: int=6000):
        """
        """
        self._app = app
        self.rules = []
        self.serializer = serializer
        self.authenticator = authenticator
        self.max_content_length = max_content_length
        svc_ctx.update_proxy_func(partial(look_up_attr, flask.g, '_svc_ctx'))

    def _common_rest_endpoint(self,
                              rule: str,
                              method: str,
                              body_params_cls: 'ModelMetaKls',
                              query_params_cls: 'QueryParametersMetaKls',
                              header_params_cls: 'HeaderParametersMetaKls',
                              extras: Optional[Dict] = None,
                              **options):
        """
        """
        self.rules.append((rule, [method]))

        def wrapped(func):
            view_func = self._view_func_wrapper(
                func,
                body_params_cls=body_params_cls,
                query_params_cls=query_params_cls,
                header_params_cls=header_params_cls)
            self._app.add_url_rule(rule=rule,
                                   endpoint=func.__name__,
                                   view_func=view_func,
                                   methods=[method],
                                   **options)
            return func

        return wrapped
    
    def create(self,
               rule: str,
               body_params_cls: 'ModelMetaKls',
               query_params_cls: 'QueryParametersMetaKls',
               header_params_cls: 'HeaderParametersMetaKls',
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(body_params_cls=body_params_cls,
                                          rule=rule,
                                          method=HTTPMethods.POST,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          options=options)
    
    def get(self,
            rule: str,
            query_params_cls: 'QueryParametersMetaKls',
            header_params_cls: 'HeaderParametersMetaKls',
            body_params_cls: Optional['ModelMetaKls'] = None,
            extras: Optional[Dict] = None,
            **options):
        """
        """
        return self._common_rest_endpoint(body_params_cls=body_params_cls,
                                          rule=rule,
                                          method=HTTPMethods.GET,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          options=options)
    
    def update(self,
               rule: str,
               body_params_cls: 'ModelMetaKls',
               query_params_cls: 'QueryParametersMetaKls',
               header_params_cls: 'HeaderParametersMetaKls',
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(body_params_cls=body_params_cls,
                                          rule=rule,
                                          method=HTTPMethods.PATCH,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          options=options)

    def delete(self,
               rule: str,
               query_params_cls: 'QueryParametersMetaKls',
               header_params_cls: 'HeaderParametersMetaKls',
               body_params_cls: Optional['ModelMetaKls'] = None,
               extras: Optional[Dict] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(body_params_cls=body_params_cls,
                                          rule=rule,
                                          method=HTTPMethods.DELETE,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          options=options)
    
    def custom(self,
               rule: str,
               verb: str,
               method: str,
               body_params_cls: 'ModelMetaKls',
               query_params_cls: 'QueryParametersMetaKls',
               header_params_cls: 'HeaderParametersMetaKls',
               extras: Optional[Dict] = None,
               **options):
        """
        """
        raise NotImplementedError

    def list(self,
             rule: str,
             query_params_cls: 'QueryParametersMetaKls',
             header_params_cls: 'HeaderParametersMetaKls',
             body_params_cls: Optional['ModelMetaKls'] = None,
             extras: Optional[Dict] = None,
             **options):
        """
        """
        return self._common_rest_endpoint(body_params_cls=body_params_cls,
                                          rule=rule,
                                          method=HTTPMethods.GET,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          options=options)

    def endpoint(self,
                 rule: str,
                 methods: List[str],
                 query_param_cls: 'QueryParametersMetaKls',
                 header_param_cls: 'HeaderParametersMetaKls',
                 body_params_cls: Optional['ModelMetaKls'] = None,
                 extras: Optional[Dict] = None,
                 **options):
        """
        """
        raise NotImplementedError

    def _view_func_wrapper(self,
                           func: Callable,
                           body_params_cls: 'ModelMetaKls',
                           query_params_cls: 'QueryParametersMetaKls',
                           header_params_cls: 'HeaderParametersMetaKls'):
        """
        """
        def setup_ctx():
            api_params = FlaskAPIParams(body_params_cls=body_params_cls,
                                        query_params_cls=query_params_cls,
                                        header_params_cls=header_params_cls)
            svc_ctx = FlaskServiceContext(svc=self)
            flask.g.api_params = api_params
            flask.g.svc_ctx = svc_ctx
        
        def authenticate():
            pass

        def wrapped(*args, **kwargs):
            svc_ctx = FlaskServiceContext(svc=self)
            flask.g.svc_ctx = svc_ctx

            auth_ctx = AuthContext()
            try:
                self.authenticator.authenticate(auth_ctx=auth_ctx,
                                                headers=flask.request.headers,
                                                query_args=flask.request.args)
            except HTTPAuthenticationError as ex:
                res = flask.make_response(ex.body_text, ex.http_status_code)
                for k in ex.headers:
                    res.headers[k] = ex.headers[k]
                return res
            svc_ctx.auth_ctx = auth_ctx

            api_params = FlaskAPIParams(body_params_cls=body_params_cls,
                                        query_params_cls=query_params_cls,
                                        header_params_cls=header_params_cls)
            svc_ctx.api_params = api_params
            
            return func()

        return wrapped

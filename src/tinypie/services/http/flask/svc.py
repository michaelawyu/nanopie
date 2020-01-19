from functools import partial
from typing import Callable, Optional

try:
    import flask
except ImportError:
    raise ImportError(
        "The Flask (https://pypi.org/project/Flask/) package is required to "
        "set up a Flask service. To install this package, run"
        "`pip install Flask`."
    )

from ..base import HTTPServiceAbstract
from .inputs import FlaskInputParameters
from ..methods import HTTPMethods
from ....serializers import JSONSerializer
from ....globals import svc_ctx, loop_up_ctx

class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self,
                 app: flask.Flask,
                 serializer: 'Serializer',
                 max_content_length: int=6000):
        """
        """
        self._app = app
        self.rules = []
        self.serializer = serializer
        _svc_ctx.set_func(partial(_loop_up_ctx, flask.g, '_svc_ctx'))

    def _common_rest_endpoint(self,
                              rule: str,
                              method: str,
                              body_params_cls: 'ModelMetaKls',
                              query_params_cls: 'QueryParametersMetaKls',
                              header_params_cls: 'HeaderParametersMetaKls',
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
               **options):
        """
        """
        raise NotImplementedError

    def list(self,
             rule: str,
             query_params_cls: 'QueryParametersMetaKls',
             header_params_cls: 'HeaderParametersMetaKls',
             body_params_cls: Optional['ModelMetaKls'] = None,
             **options):
        """
        """
        raise NotImplementedError

    def endpoint(self,
                 rule: str,
                 query_param_cls: 'QueryParametersMetaKls',
                 header_param_cls: 'HeaderParametersMetaKls',
                 body_params_cls: Optional['ModelMetaKls'] = None,
                 **options):
        """
        """
        raise NotImplementedError

    def add_resource(self, resource: 'Resource'):
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
        def wrapped(*args, **kwargs):
            inputs = FlaskInputParameters(request=flask.request,
                                          body_params_cls=body_params_cls,
                                          query_params_cls=query_params_cls,
                                          header_params_cls=header_params_cls,
                                          serializer=self.serializer)
            return func(inputs)

        return wrapped

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
from .inputs import HTTPInputParameters
from ..methods import HTTPMethods
from ....misc.utils import prepare_url_rule_from_resource

class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self, app: flask.Flask):
        """
        """
        self._app = app
        self.rules = []

    def _common_rest_endpoint(self,
                              resource_cls: 'ResourceMetaKls',
                              resource_group: bool,
                              method: str,
                              query_param_cls: 'ModelMetaKls',
                              header_param_cls: 'ModelMetaKls',
                              rule: Optional[str],
                              **options):
        """
        """
        if not rule:
            rule = prepare_url_rule_from_resource(resource_cls, resource_group)
            self.rules.append((rule, methods))

        def wrapped(func):
            view_func = self._view_func_wrapper(func)
            self._app.add_url_rule(rule=rule,
                                   endpoint=func.__name__,
                                   view_func=view_func,
                                   methods=methods,
                                   **options)
            return func

        return wrapped
    
    def create(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          resource_group=True,
                                          method=HTTPMethods.POST,
                                          query_param_cls=query_param_cls,
                                          header_param_cls=header_param_cls,
                                          rule=rule,
                                          options=options)
    
    def get(self,
            resource_cls: 'ResourceMetaKls',
            query_param_cls: 'ModelMetaKls',
            header_param_cls: 'ModelMetaKls',
            rule: Optional[str] = None,
            **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          resource_group=False,
                                          method=HTTPMethods.GET,
                                          query_param_cls=query_param_cls,
                                          header_param_cls=header_param_cls,
                                          rule=rule,
                                          options=options)
    
    def update(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          resource_group=False,
                                          method=HTTPMethods.PATCH,
                                          query_param_cls=query_param_cls,
                                          header_param_cls=header_param_cls,
                                          rule=rule,
                                          options=options)

    def delete(self,
               resource_cls: 'ResourceMetaKls',
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str] = None,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          resource_group=False,
                                          method=HTTPMethods.DELETE,
                                          query_param_cls=query_param_cls,
                                          header_param_cls=header_param_cls,
                                          rule=rule,
                                          options=options)
    
    def custom(self,
               resource_cls: 'ResourceMetaKls',
               resource_group: bool,
               verb: str,
               method: str,
               query_param_cls: 'ModelMetaKls',
               header_param_cls: 'ModelMetaKls',
               rule: Optional[str],
               **options):
        """
        """
        raise NotImplementedError

    def list(self,
             resource_cls: 'ResourceMetaKls',
             query_param_cls: 'ModelMetaKls',
             header_param_cls: 'ModelMetaKls',
             rule: Optional[str],
             **options):
        """
        """
        raise NotImplementedError

    def add_resource(self, resource: 'Resource'):
        """
        """
        raise NotImplementedError

    @staticmethod
    def _view_func_wrapper(func):
        """
        """
        def wrapped(*args, **kwargs):
            pass

        return wrapped

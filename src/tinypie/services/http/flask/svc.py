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


class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self,
                 app: flask.Flask,
                 serializer: 'Serializer'):
        """
        """
        self._app = app
        self.rules = []
        self.serializer = serializer

    def _common_rest_endpoint(self,
                              resource_cls: 'ModelMetaKls',
                              rule: str,
                              method: str,
                              **options):
        """
        """
        self.rules.append((rule, [method]))

        def wrapped(func):
            view_func = self._view_func_wrapper(
                func,
                resource_cls=resource_cls)
            self._app.add_url_rule(rule=rule,
                                   endpoint=func.__name__,
                                   view_func=view_func,
                                   methods=[method],
                                   **options)
            return func

        return wrapped
    
    def create(self,
               resource_cls: 'ModelMetaKls',
               rule: str,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          rule=rule,
                                          method=HTTPMethods.POST,
                                          options=options)
    
    def get(self,
            resource_cls: 'ModelMetaKls',
            rule: str,
            **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          rule=rule,
                                          method=HTTPMethods.GET,
                                          options=options)
    
    def update(self,
               resource_cls: 'ModelMetaKls',
               rule: str,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          rule=rule,
                                          method=HTTPMethods.PATCH,
                                          options=options)

    def delete(self,
               resource_cls: 'ModelMetaKls',
               rule: str,
               **options):
        """
        """
        return self._common_rest_endpoint(resource_cls=resource_cls,
                                          rule=rule,
                                          method=HTTPMethods.DELETE,
                                          options=options)
    
    def custom(self,
               resource_cls: 'ModelMetaKls',
               rule: str,
               verb: str,
               method: str,
               **options):
        """
        """
        raise NotImplementedError

    def list(self,
             resource_cls: 'ModelMetaKls',
             rule: str,
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
                           resource_cls: 'ModelMetaKls'):
        """
        """
        def wrapped(*args, **kwargs):
            inputs = FlaskInputParameters(request=flask.request,
                                          resource_cls=resource_cls,
                                          serializer=self.serializer)
            return func(inputs)

        return wrapped

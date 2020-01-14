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
from ....misc.utils import prepare_url_rule_from_resource
from ....serializers.generic import JSONSerializer
from ....serializers.http import (
    URLEncodingQueryStringSerializer,
    StandardHeaderSerializer
)


class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self,
                 app: flask.Flask,
                 body_serializer: 'SerializerAbstract' = JSONSerializer(),
                 query_str_serializer: 'SerializerAbstract' = URLEncodingQueryStringSerializer(),
                 header_serialzier: 'SerializerAbstract' = StandardHeaderSerializer()):
        """
        """
        self._app = app
        self.rules = []
        self.body_serializer = body_serializer
        self.query_str_serializer = query_str_serializer
        self.header_serializer = header_serialzier

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
            view_func = self._view_func_wrapper(
                func,
                resource_cls=resource_cls,
                query_param_cls=query_param_cls,
                header_param_cls=header_param_cls)
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

    def _view_func_wrapper(self,
                           func: Callable,
                           resource_cls: 'ResourceMetaKls',
                           query_param_cls: 'ModelMetaKls',
                           header_param_cls: 'ModelMetaKls'):
        """
        """
        def wrapped(*args, **kwargs):
            inputs = FlaskInputParameters(request=flask.request,
                                          resource_cls=resource_cls,
                                          query_param_cls=query_param_cls,
                                          header_param_cls=header_param_cls,
                                          body_serializer=self.body_serializer,
                                          query_str_serializer=self.query_str_serializer,
                                          header_serializer=self.header_serializer)
            return func(inputs)

        return wrapped

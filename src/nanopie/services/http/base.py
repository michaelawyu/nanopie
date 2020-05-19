from abc import abstractmethod
from typing import Callable, Dict, Optional

from ..base import RPCService
from .foundation import HTTPFoundationHandler
from ...handler import SimpleHandler
from .io import HTTPEndpoint
from .methods import HTTPMethods
from ...serialization.http import HTTPSerializationHandler
from ...serialization.helpers import JSONSerializationHelper


class HTTPService(RPCService):
    """
    """

    def __init__(
        self,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        serialization_helper: Optional[
            "SerializationHelper"
        ] = JSONSerializationHelper(),
        max_content_length: Optional[int] = 6000,
    ):
        """
        """
        super().__init__(
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            serialization_helper=serialization_helper,
            max_content_length=max_content_length,
        )

    @abstractmethod
    def add_endpoint(self, endpoint: "HTTPEndpoint", **kwargs):
        pass

    def _rest_endpoint(
        self,
        name: str,
        rule: str,
        method: str,
        serialization_handler: Optional["SerializationHandler"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        entrypoint = HTTPFoundationHandler(max_content_length=self.max_content_length)

        handler = entrypoint
        if authn_handler:
            handler = handler.wraps(authn_handler)
        elif self.authn_handler:
            handler = handler.wraps(self.authn_handler)

        if logging_handler:
            handler = handler.wraps(logging_handler)
        elif self.logging_handler:
            handler = handler.wraps(self.logging_handler)

        if tracing_handler:
            handler = handler.wraps(tracing_handler)
        elif self.tracing_handler:
            handler = handler.wraps(self.tracing_handler)

        if serialization_handler:
            handler = handler.wraps(serialization_handler)
        elif self.serialization_handler:
            handler = handler.wraps(self.serialization_handler)

        def wrapper(func):
            simple_handler = SimpleHandler(func=func)
            handler.wraps(simple_handler)
            endpoint = HTTPEndpoint(
                name=name,
                rule=rule,
                method=method,
                entrypoint=entrypoint,
                extras=extras,
            )
            self.add_endpoint(endpoint, **options)
            return func

        return wrapper

    def create(
        self,
        name: str,
        rule: str,
        data_cls: "ModelMetaCls",
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.POST,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_create_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.create(*args, **kwargs)(func)

    def get(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.GET,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_get_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.get(*args, **kwargs)(func)

    def update(
        self,
        name: str,
        rule: str,
        data_cls: "ModelMetaCls",
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.PATCH,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_update_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.update(*args, **kwargs)(func)

    def delete(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.DELETE,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_delete_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        return self.delete(*args, **kwargs)(func)

    def list(
        self,
        name: str,
        rule: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=HTTPMethods.GET,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_list_endpoint(self, *args, func, **kwargs):
        """
        """
        return self.list(*args, **kwargs)(func)

    def custom(
        self,
        name: str,
        rule: str,
        verb: str,
        method: str,
        data_cls: Optional["ModelMetaCls"] = None,
        headers_cls: Optional["ModelMetaCls"] = None,
        query_args_cls: Optional["ModelMetaCls"] = None,
        authn_handler: Optional["AuthenticationHandler"] = None,
        logging_handler: Optional["LoggingHandler"] = None,
        tracing_handler: Optional["TracingHandler"] = None,
        extras: Optional[Dict] = None,
        **options
    ):
        """
        """
        if rule.endswith("/"):
            rule = rule[:-1]
        rule = "{}:{}".format(rule, verb)

        if method not in HTTPMethods.supported_methods:
            raise ValueError(
                "{} is not a supported HTTP method ({}).".format(
                    method, HTTPMethods.supported_methods
                )
            )

        serialization_handler = HTTPSerializationHandler(
            headers_cls=headers_cls,
            query_args_cls=query_args_cls,
            data_cls=data_cls,
            serialization_helper=self.serialization_helper,
        )
        return self._rest_endpoint(
            name=name,
            rule=rule,
            method=method,
            serialization_handler=serialization_handler,
            authn_handler=authn_handler,
            logging_handler=logging_handler,
            tracing_handler=tracing_handler,
            extras=extras,
            **options
        )

    def add_custom_endpoint(self, *args, func: Callable, **kwargs):
        """
        """
        self.custom(*args, **kwargs)(func)

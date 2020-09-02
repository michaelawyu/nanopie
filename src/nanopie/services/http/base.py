"""This module includes the base class for nanopie HTTP services.
"""

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
    """The base class for all HTTP services."""

    def __init__(
        self,
        serialization_helper: Optional[
            "SerializationHelper"
        ] = JSONSerializationHelper(),
        *args,
        **kwargs
    ):
        """Initializes an HTTP service.

        Args:
            serialization_helper (SerializationHelper, Optional): The default
                serialization helper for all endpoints.
            *args: Other positional arguments. See `RPCService`.
            **kwargs: Other keyword arguments. See `RPCService`.
        """
        super().__init__(*args, serialization_helper=serialization_helper, **kwargs)

    @abstractmethod
    def add_endpoint(self, endpoint: "HTTPEndpoint", **kwargs):
        """See the method `RPCService.add_endpoint`."""
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
        """Adds a RESTful endpoint.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            method (str): The HTTP method associated with the endpoint.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            serialization_helper (SerializationHelper, Optional): The
                serialization helper for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.
        """

        entrypoint = HTTPFoundationHandler(max_content_length=self.max_content_length)
        handler = entrypoint

        if authn_handler:
            handler = handler.add_route(name=name, handler=authn_handler)
        elif self.authn_handler:
            handler = handler.add_route(name=name, handler=self.authn_handler)

        if logging_handler:
            handler = handler.add_route(name=name, handler=logging_handler)
        elif self.logging_handler:
            handler = handler.add_route(name=name, handler=self.logging_handler)

        if tracing_handler:
            handler = handler.add_route(name=name, handler=tracing_handler)
        elif self.tracing_handler:
            handler = handler.add_route(name=name, handler=self.tracing_handler)

        if serialization_handler:
            handler = handler.add_route(name=name, handler=serialization_handler)

        def wrapper(func):
            simple_handler = SimpleHandler(func=func)
            handler.add_route(name=name, handler=simple_handler)
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
        """The decorator for adding a CREATE endpoint.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            data_cls (ModelMetaCls): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.create(name="create_user", rule="/users/", ...)
        def create_user():
            # Custom logic
        ```
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
        """Adds a CREATE endpoint.

        Args:
            func (Callable): The function to process the request.
            *args: Other positional arguments. See the method `create`.
            **kwargs: Other keyword arguments. See the method `create`.
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
        """The decorator for adding a GET method.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            data_cls (ModelMetaCls, Optional): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.get(name="get_user", rule="/users/{int:user_id}", ...)
        def get_user(user_id):
            # Custom logic
        ```
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
        """Adds a GET endpoint.

        Args:
           func (Callable): The function to process the request.
           *args: Other positional arguments. See the method `get`.
           **kwargs: Other keyword arguments. See the method `get`.
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
        """The decorator for adding an UPDATE method.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            data_cls (ModelMetaCls): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.update(name="update_user", rule="/users/{int:user_id}", ...)
        def update_user(user_id):
            # Custom logic
        ```
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
        """Adds an UPDATE endpoint.

        Args:
           func (Callable): The function to process the request.
           *args: Other positional arguments. See the method `update`.
           **kwargs: Other keyword arguments. See the method `update`.
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
        """The decorator for adding a DELETE method.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            data_cls (ModelMetaCls, Optional): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.delete(name="delete_user", rule="/users/{int:user_id}", ...)
        def delete_user(user_id):
            # Custom logic
        ```
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
        """Adds a DELETE endpoint.

        Args:
           func (Callable): The function to process the request.
           *args: Other positional arguments. See the method `delete`.
           **kwargs: Other keyword arguments. See the method `delete`.
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
        """The decorator for adding a LIST method.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            data_cls (ModelMetaCls, Optional): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.list(name="list_users", rule="/users/", ...)
        def list_users():
            # Custom logic
        ```
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
        """Adds a LIST endpoint.

        Args:
           func (Callable): The function to process the request.
           *args: Other positional arguments. See the method `list`.
           **kwargs: Other keyword arguments. See the method `list`.
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
        """The decorator for adding a custom method.

        Args:
            name (str): The name of the endpoint.
            rule (str): The rule associated with the endpoint.
            verb (str): The HTTP verb associated with the endpoint.
            data_cls (ModelMetaCls, Optional): The data model for the request
                payload (body).
            headers_cls (ModelMetaCls, Optional): The data model for the headers
                of the request.
            query_args_cls (ModelMetaCls, Optional): The data model for the
                query arguments in the URI of the request.
            authn_handler (AuthenticationHandler, Optional): The
                authentication handler for this endpoint.
            logging_handler (LoggingHandler, Optional): The logging handler
                for this endpoint.
            tracing_handler (TracingHandler, Optional): The tracing handler
                for this endpoint.
            extras (Dict, Optional): Additional information about the endpoint.
            **options: Other keyword arguments for configuring this endpoint.
                They vary according to the transport used.

        Usage:
        ```Python
        @svc.custom(name="verify_user",
                    rule="/users/{int:user_id}",
                    verb="GET",
                    ...)
        def verify_user(user_id):
            # Custom logic
        ```
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
        """ "Adds a custom endpoint.

        Args:
           func (Callable): The function to process the request.
           *args: Other positional arguments. See the method `custom`.
           **kwargs: Other keyword arguments. See the method `custom`.
        """
        self.custom(*args, **kwargs)(func)

"""This module includes the base class nanopie uses for handling requests and
a subclass of it that performs simple, function-based handling.

nanopie uses `Handler` instances to process requests and prepare responses
in a microservice/API service. Each handler performs a specific task, such
as authentication, logging, tracing, and serialization/deserialization.
Handlers can be chained together, which allows a handler to do its job,
pass the baton to another handler, and wrap everything up when the chained
handler(s) finishes processing.
"""

from typing import Callable

from .globals import endpoint


class Handler:
    """The base class for all handlers."""

    def __init__(self):
        """Initializes the handler."""
        self._routes = {}

    def __call__(self, *args, **kwargs):
        """Runs the handler.

        Handlers will look up current endpoint via the endpoint global proxy
        (see globals.py) and routes to the next chained handler.

        Handlers are transparent; it will pass any argument it receives to
        the next handler.

        Args:
            *args: Positional arguments to pass to the next chained handler.
            **kwargs: Keyword arguments to pass to the next chained handler.
        """
        if self._routes:
            name = endpoint.name
            if self._routes.get(name):
                return self._routes[name](
                    *args, **kwargs
                )  # pylint: disable=not-callable
            else:
                raise RuntimeError("Route is not found.")

    def add_route(self, name: str, handler: "Handler"):
        """Specifies a route to a handler.

        Args:
            name (str): The name of the route, usually it is the name of an
                endpoint.
            handler (Handler): The handler to chain.
        """
        if self._routes.get(name):
            raise RuntimeError("A route with the same name already exists.")

        self._routes[name] = handler
        return handler


class SimpleHandler(Handler):
    """A handler that simply runs a function."""

    def __init__(self, func: Callable):
        """Initializes the handler.

        Args:
            func (Callable): The function to run.
        """
        self.func = func
        super().__init__()

    def __call__(self, *args, **kwargs):
        """Runs the handler.

        Args:
            *args: Positional arguments to pass to the next chained handler.
            **kwargs: Keyword arguments to pass to the next chained handler.
        """
        res = self.func(*args, **kwargs)
        if res != None:
            return res
        else:
            return super().__call__(*args, **kwargs)

from typing import Callable

from .globals import endpoint


class Handler:
    """
    """

    def __init__(self):
        """
        """
        self.routes = {}

    def __call__(self, *args, **kwargs):
        """
        """
        if self.routes:
            name = endpoint.name
            if self.routes.get(name):
                return self.routes[name](
                    *args, **kwargs
                )  # pylint: disable=not-callable
            else:
                raise RuntimeError("Route is not found.")

    def add_route(self, name: str, handler: "Handler"):
        """
        """
        if self.routes.get(name):
            raise RuntimeError("A route with the same name already exists.")

        self.routes[name] = handler
        return handler


class SimpleHandler(Handler):
    """
    """

    def __init__(self, func: Callable):
        """
        """
        self.func = func
        super().__init__()

    def __call__(self, *args, **kwargs):
        res = self.func(*args, **kwargs)
        if res != None:
            return res
        else:
            return super().__call__(*args, **kwargs)

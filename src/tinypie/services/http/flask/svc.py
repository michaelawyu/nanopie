from typing import Callable

try:
    import flask
except ImportError:
    raise ImportError(
        "The Flask (https://pypi.org/project/Flask/) package is required to "
        "set up a Flask service. To install this package, run"
        "`pip install Flask`."
    )

from ..base import HTTPServiceAbstract
from ....entities.model import Model

class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self, app: flask.Flask):
        """
        """
        self._app = app

    def create(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        raise NotImplementedError

    def get(self,
            resource: Model,
            func: Callable) -> Callable:
        """
        """
        raise NotImplementedError

    def update(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        raise NotImplementedError

    def delete(self,
               resource: Model,
               func: Callable) -> Callable:
        """
        """
        raise NotImplementedError

    def list(self,
             resource: Model,
             func: Callable) -> Callable:
        """
        """
        raise NotImplementedError

    def add_resource(self, resource: Model):
        """
        """
        raise NotImplementedError

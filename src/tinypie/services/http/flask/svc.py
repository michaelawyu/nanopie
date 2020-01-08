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

class FlaskService(HTTPServiceAbstract):
    """
    """
    def __init__(self, app: flask.Flask):
        """
        """
        self._app = app

    def create(self,
               resource: 'Resource',
               path: Optional[str]):
        """
        """
        raise NotImplementedError

    def get(self,
            resource: 'Resource',
            path: Optional[str]):
        """
        """
        raise NotImplementedError

    def update(self,
               resource: 'Resource',
               path: Optional[str]):
        """
        """
        raise NotImplementedError

    def delete(self,
               resource: 'Resource',
               path: Optional[str]):
        """
        """
        raise NotImplementedError

    def list(self,
             resource: 'Resource',
             path: Optional[str]):
        """
        """
        raise NotImplementedError

    def add_resource(self, resource: 'Resource'):
        """
        """
        raise NotImplementedError

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

    def create(self,
               resource: 'Resource',
               rule: Optional[str],
               **options):
        """
        """
        methods = [HTTPMethods.POST]

        if not rule:
            rule = prepare_url_rule_from_resource(resource)
            self.rules.append((rule, methods))

        def wrapped(func):
            view_func = self._view_func_wrapper(func)
            self._app.add_url_rule(rule, func.__name__, view_func, **options)
            return func

        return wrapped

    def get(self,
            resource: 'Resource',
            rule: Optional[str]):
        """
        """
        raise NotImplementedError

    def update(self,
               resource: 'Resource',
               rule: Optional[str]):
        """
        """
        raise NotImplementedError

    def delete(self,
               resource: 'Resource',
               rule: Optional[str]):
        """
        """
        raise NotImplementedError

    def list(self,
             resource: 'Resource',
             rule: Optional[str]):
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
        def wrapped():
            pass

        return wrapped

from functools import partial

try:
    import flask

    FLASK_INSTALLED = True
except ImportError:
    FLASK_INSTALLED = False

from .base import HTTPRequest, HTTPResponse, HTTPService
from ...misc.errors import ServiceError


class FlaskService(HTTPService):
    """
    """

    def __init__(self, app: "flask.Flask", **kwargs):
        """
        """
        if not FLASK_INSTALLED:
            raise ImportError(
                "The flask (https://pypi.org/project/flask/)"
                "package is required to use flask with nanopie. "
                "To install this package, run "
                "`pip install pyjwt`."
            )

        self._app = app

        super().__init__(**kwargs)

    def add_endpoint(self, endpoint: "HTTPEndpoint", **kwargs):
        """
        """
        svc = self

        def view_func(*args, **kwargs):
            request = HTTPRequest(
                url=partial(getattr, flask.request, "url"),
                headers=partial(getattr, flask.request, "headers"),
                content_length=partial(getattr, flask.request, "content_length"),
                mime_type=partial(getattr, flask.request, "mime_type"),
                query_args=partial(getattr, flask.request, "args"),
                binary_data=partial(flask.request.get_data),
                text_data=partial(flask.request.get_data, as_text=True),
            )
            svc_ctx = {}
            flask.g._svc_ctx = svc_ctx  # pylint: disable=protected-access
            svc_ctx["svc"] = svc
            svc_ctx["endpoint"] = endpoint
            svc_ctx["request"] = request

            try:
                res = endpoint.entrypoint(*args, **kwargs)
            except ServiceError as ex:
                if ex.response:
                    res = ex.response
                else:
                    raise ex

            if isinstance(res, HTTPResponse):
                return flask.make_response((res.data, res.status_code, res.headers))

            return res

        self._app.add_url_rule(
            rule=endpoint.rule,
            endpoint=endpoint.name,
            view_func=view_func,
            methods=[endpoint.method],
            **kwargs
        )

        self.endpoints.append(endpoint)

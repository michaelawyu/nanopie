from functools import partial

try:
    import flask

    FLASK_INSTALLED = True
except ImportError:
    FLASK_INSTALLED = False

from .base import HTTPService
from ...globals import look_up_attr, svc_ctx, endpoint
from .io import HTTPRequest, HTTPResponse
from ...logger import logger
from ...misc.errors import ServiceError


class FlaskService(HTTPService):
    """The class for HTTP services with Flask apps as transport."""

    def __init__(self, *args, app: "flask.Flask", **kwargs):
        """Initializes a Flask based HTTP service.

        Args:
            app (flask.Flask): A Flask app.
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary keyword arguments.
        """
        if not FLASK_INSTALLED:
            raise ImportError(
                "The flask (https://pypi.org/project/flask/)"
                "package is required to use flask with nanopie. "
                "To install this package, run "
                "`pip install pyjwt`."
            )

        self._app = app

        super().__init__(*args, **kwargs)

    def add_endpoint(self, endpoint: "HTTPEndpoint", **kwargs):
        """Adds an HTTP endpoint.

        Args:
            endpoint (HTTPEndpoint): An HTTP endpoint.
            **kwargs: Arbitrary keyword arguments.
        """
        svc = self

        def view_func(*args, **kwargs):
            request = HTTPRequest(
                url=partial(getattr, flask.request, "url"),
                headers=partial(
                    lambda x: dict(x()), partial(getattr, flask.request, "headers")
                ),
                content_length=partial(getattr, flask.request, "content_length"),
                mime_type=partial(getattr, flask.request, "mimetype"),
                query_args=partial(getattr, flask.request, "args"),
                binary_data=partial(flask.request.get_data),
                text_data=partial(flask.request.get_data, as_text=True),
            )
            ctx = {}
            flask.g._svc_ctx = ctx  # pylint: disable=protected-access
            svc_ctx.update_proxy_func(
                partial(look_up_attr, ctx=flask.g, name="_svc_ctx")
            )

            ctx["svc"] = svc
            ctx["endpoint"] = endpoint
            ctx["request"] = request

            try:
                res = endpoint.entrypoint(*args, **kwargs)
            except ServiceError as ex:
                if ex.response:
                    res = ex.response
                    logger.error(ex)
                else:
                    raise ex

            if isinstance(res, HTTPResponse):
                flask_res = flask.make_response(
                    (res.data, res.status_code, res.headers)
                )
                flask_res.mimetype = res.mime_type
                return flask_res

            return res

        self._app.add_url_rule(
            rule=endpoint.rule,
            endpoint=endpoint.name,
            view_func=view_func,
            methods=[endpoint.method],
            **kwargs
        )

        if self.endpoints.get(endpoint.name) == None:
            self.endpoints[endpoint.name] = endpoint
        else:
            raise RuntimeError("An endpoint with the same name already exists.")

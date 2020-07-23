from functools import partial
from unittest.mock import MagicMock

from nanopie import Handler, SimpleHandler
from nanopie.globals import endpoint
from nanopie.services.base import RPCEndpoint


class DummyHandler(Handler):
    def __call__(self, *args, **kwargs):
        return "This is a dummy handler."


def test_handler():
    handler = Handler()

    assert handler() == None


def test_handler_routes(setup_ctx):
    handler = Handler()
    dummy_handler = DummyHandler()

    handler.add_route(name="dummy_handler", handler=dummy_handler)

    endpoint.name = "dummy_handler"  # pylint: disable=assigning-non-slot

    assert handler() == "This is a dummy handler."


def test_simple_handler():
    def func():
        return "This is a simple handler."

    simple_handler = SimpleHandler(func=func)

    assert simple_handler() == "This is a simple handler."


def test_simple_handler_routes(setup_ctx):
    def func():
        pass

    dummy_handler = DummyHandler()

    simple_handler = SimpleHandler(func=func)
    simple_handler.add_route(name="dummy_handler", handler=dummy_handler)

    endpoint.name = "dummy_handler"  # pylint: disable=assigning-non-slot

    assert simple_handler() == "This is a dummy handler."

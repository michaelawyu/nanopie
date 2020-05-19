from nanopie import Handler, SimpleHandler


class DummyHandler(Handler):
    def __call__(self, *args, **kwargs):
        return "This is a dummy handler."


def test_handler():
    handler = Handler()

    assert handler.wrapped == None
    assert handler() == None


def test_handler_wraps():
    handler = Handler()
    dummy_handler = DummyHandler()

    handler.wraps(dummy_handler)

    assert handler.wrapped == dummy_handler
    assert handler() == "This is a dummy handler."


def test_simple_handler():
    def func():
        return "This is a simple handler."

    simple_handler = SimpleHandler(func=func)

    assert simple_handler() == "This is a simple handler."


def test_simple_handler_wraps():
    def func():
        pass

    dummy_handler = DummyHandler()

    simple_handler = SimpleHandler(func=func)
    simple_handler.wraps(dummy_handler)

    assert simple_handler() == "This is a dummy handler."

"""This module includes the proxies nanopie uses.

A proxy forwards calls to its wrapped object. nanopie uses proxies to
provide global access to contextual key data and attributes a
microservice/API service may use while processing the a request,
such as the parsed payload and the current active endpoint. For more
information, see `globals.py`.

The proxies work in the same way as the proxies (request, g, etc.) in
Flask and quart.
"""

import copy
from typing import Any, Callable, Dict


class GenericProxy:
    """A proxy that simply forwards all the calls to the wrapped object."""

    __slots__ = "_proxy_func"

    def __init__(self, proxy_func: Callable):
        """Initializes a GenericProxy.

        Args:
            proxy_func (Callable): a function or a callable object that the
                proxy calls to get the wrapped object.
        """
        object.__setattr__(self, "_proxy_func", proxy_func)

    def update_proxy_func(self, proxy_func: Callable):
        """Updates the proxy_func associated with the proxy.

        Args:
            proxy_func (Callable): a function or a callable object that the
                proxy calls to get the wrapped object.
        """
        object.__setattr__(self, "_proxy_func", proxy_func)

    @property
    def wrapped(self) -> object:
        """Any: the wrapped object."""
        return object.__getattribute__(self, "_proxy_func")()

    @property
    def __dict__(self) -> Dict[str, Any]:
        """Calls the __dict__ magic method of the wrapped object."""
        try:
            return self.wrapped.__dict__
        except RuntimeError:
            raise AttributeError("__dict__")

    def __repr__(self) -> str:
        """Calls the __repr__ magic method of the wrapped object."""
        try:
            wrapped = self.wrapped
        except RuntimeError:
            return "<%s unbound>" % self.__class__.__name__

        return repr(wrapped)

    def __bool__(self) -> bool:
        """Calls the __bool__ magic method of the wrapped object."""
        try:
            return bool(self.wrapped)
        except RuntimeError:
            return False

    def __dir__(self) -> Any:
        """Calls the __dir__ magic method of the wrapped object."""
        try:
            return dir(self.wrapped)
        except RuntimeError:
            return []

    def __getattr__(self, name: str) -> Any:
        """Calls the __getattr__ magic method of the wrapped object."""
        if name == "__members":
            return dir(self.wrapped)

        return object.__getattribute__(self.wrapped, name)

    def __setitem__(self, key: Any, value: Any) -> Any:
        """Calls the __setitem__ magic method of the wrapped object."""
        self.wrapped[key] = value

    def __delitem__(self, key: Any) -> Any:
        """Calls the __delitem__ magic method of the wrapped object."""
        del self.wrapped[key]

    async def __aiter__(self) -> Any:
        """Calls the __aiter__ magic method of the wrapped object."""
        async for x in self.wrapped:
            yield x

    __setattr__ = lambda x, n, v: object.__setattr__(x.wrapped, n, v)
    __delattr__ = lambda x, n: object.__delattr__(x.wrapped, n)
    __str__ = lambda x: str(x.wrapped)
    __lt__ = lambda x, o: x.wrapped < o
    __le__ = lambda x, o: x.wrapped <= o
    __eq__ = lambda x, o: x.wrapped == o
    __ne__ = lambda x, o: x.wrapped != o
    __gt__ = lambda x, o: x.wrapped > o
    __ge__ = lambda x, o: x.wrapped >= o
    __hash__ = lambda x: hash(x.wrapped)
    __call__ = lambda x, *a, **kw: x.wrapped(*a, **kw)
    __len__ = lambda x: len(x.wrapped)
    __getitem__ = lambda x, i: x.wrapped[i]
    __iter__ = lambda x: iter(x.wrapped)
    __contains__ = lambda x, i: i in x.wrapped
    __add__ = lambda x, o: x.wrapped + o
    __sub__ = lambda x, o: x.wrapped - o
    __mul__ = lambda x, o: x.wrapped * o
    __floordiv__ = lambda x, o: x.wrapped // o
    __mod__ = lambda x, o: x.wrapped % o
    __divmod__ = lambda x, o: x.wrapped.__divmod__(o)
    __pow__ = lambda x, o: x.wrapped ** o
    __lshift__ = lambda x, o: x.wrapped << o
    __rshift__ = lambda x, o: x.wrapped >> o
    __and__ = lambda x, o: x.wrapped & o
    __xor__ = lambda x, o: x.wrapped ^ o
    __or__ = lambda x, o: x.wrapped | o
    __div__ = lambda x, o: x.wrapped.__div__(o)
    __truediv__ = lambda x, o: x.wrapped.__truediv__(o)
    __neg__ = lambda x: -(x.wrapped)
    __pos__ = lambda x: +(x.wrapped)
    __abs__ = lambda x: abs(x.wrapped)
    __invert__ = lambda x: ~(x.wrapped)
    __complex__ = lambda x: complex(x.wrapped)
    __int__ = lambda x: int(x.wrapped)
    __float__ = lambda x: float(x.wrapped)
    __oct__ = lambda x: oct(x.wrapped)
    __hex__ = lambda x: hex(x.wrapped)
    __index__ = lambda x: x.wrapped.__index__()
    __coerce__ = lambda x, o: x.wrapped.__coerce__(
        x, o
    )  # pylint: disable=unnecessary-lambda
    __enter__ = lambda x: x.wrapped.__enter__()
    __exit__ = lambda x, *a, **kw: x.wrapped.__exit__(*a, **kw)
    __radd__ = lambda x, o: o + x.wrapped
    __rsub__ = lambda x, o: o - x.wrapped
    __rmul__ = lambda x, o: o * x.wrapped
    __rdiv__ = lambda x, o: o / x.wrapped
    __rtruediv__ = __rdiv__
    __rfloordiv__ = lambda x, o: o // x.wrapped
    __rmod__ = lambda x, o: o % x.wrapped
    __rdivmod__ = lambda x, o: x.wrapped.__rdivmod__(o)
    __copy__ = lambda x: copy.copy(x.wrapped)
    __deepcopy__ = lambda x, memo: copy.deepcopy(x.wrapped, memo)
    __await__ = lambda x: x.wrapped.__await__()

from typing import Any, Callable, Dict, Optional

class Proxy:
    """
    """
    __slots__ = ('_callable', '__dict__')

    def __init__(self, func: Callable, name: Optional[str] = None):
        """
        """
        object.__setattr__(self, '_callable', func)
        object.__setattr__(self, '__name__', name)
    
    def set_func(self, func: Callable) -> Any:
        """
        """
        object.__setattr__(self, '_callable', func)
    
    def _get_object(self) -> Any:
        """
        """
        return object.__getattribute__(self, '_callable')()
    
    def __getattr__(self, name: str) -> Any:
        """
        """
        if name == '__members__':
            return dir(self._get_object())
        return getattr(self._get_object(), name)
    
    def __setattr__(self, name: str, value: Any):
        """
        """
        setattr(self._get_object(), name, value)

    @property
    def __dict__(self) -> Dict[str, Any]:
        """
        """
        try:
            return self._get_object().__dict__
        except RuntimeError:
            raise AttributeError("__dict__")
    
    def __repr__(self) -> str:
        """
        """
        try:
            obj = self._get_object()
        except RuntimeError:
            return '<%s unbound>' % self.__class__.__name__
        return repr(obj)
    
    def __bool__(self) -> bool:
        """
        """
        try:
            return bool(self._get_object())
        except RuntimeError:
            return False

    def __dir__(self) -> Any:
        """
        """
        try:
            return dir(self._get_object())
        except RuntimeError:
            return []

    def __setitem__(self, key: Any, value: Any) -> Any:
        """
        """
        self._get_object()[key] = value

    def __delitem__(self, key: Any) -> Any:
        """
        """
        del self._get_object()[key]

    async def __aiter__(self) -> Any:
        """
        """
        async for x in self._get_object():
            yield x

    __delattr__ = lambda x, n: delattr(x._get_object(), n)  # type: ignore # noqa: E731
    __str__ = lambda x: str(x._get_object())  # type: ignore # noqa: E731
    __lt__ = lambda x, o: x._get_object() < o  # noqa: E731
    __le__ = lambda x, o: x._get_object() <= o  # noqa: E731
    __eq__ = lambda x, o: x._get_object() == o  # type: ignore # noqa: E731
    __ne__ = lambda x, o: x._get_object() != o  # type: ignore # noqa: E731
    __gt__ = lambda x, o: x._get_object() > o  # noqa: E731
    __ge__ = lambda x, o: x._get_object() >= o  # noqa: E731
    __hash__ = lambda x: hash(x._get_object())  # type: ignore # noqa: E731
    __call__ = lambda x, *a, **kw: x._get_object()(*a, **kw)  # noqa: E731
    __len__ = lambda x: len(x._get_object())  # noqa: E731
    __getitem__ = lambda x, i: x._get_object()[i]  # noqa: E731
    __iter__ = lambda x: iter(x._get_object())  # noqa: E731
    __contains__ = lambda x, i: i in x._get_object()  # noqa: E731
    __add__ = lambda x, o: x._get_object() + o  # noqa: E731
    __sub__ = lambda x, o: x._get_object() - o  # noqa: E731
    __mul__ = lambda x, o: x._get_object() * o  # noqa: E731
    __floordiv__ = lambda x, o: x._get_object() // o  # noqa: E731
    __mod__ = lambda x, o: x._get_object() % o  # noqa: E731
    __divmod__ = lambda x, o: x._get_object().__divmod__(o)  # noqa: E731
    __pow__ = lambda x, o: x._get_object() ** o  # noqa: E731
    __lshift__ = lambda x, o: x._get_object() << o  # noqa: E731
    __rshift__ = lambda x, o: x._get_object() >> o  # noqa: E731
    __and__ = lambda x, o: x._get_object() & o  # noqa: E731
    __xor__ = lambda x, o: x._get_object() ^ o  # noqa: E731
    __or__ = lambda x, o: x._get_object() | o  # noqa: E731
    __div__ = lambda x, o: x._get_object().__div__(o)  # noqa: E731
    __truediv__ = lambda x, o: x._get_object().__truediv__(o)  # noqa: E731
    __neg__ = lambda x: -(x._get_object())  # noqa: E731
    __pos__ = lambda x: +(x._get_object())  # noqa: E731
    __abs__ = lambda x: abs(x._get_object())  # noqa: E731
    __invert__ = lambda x: ~(x._get_object())  # noqa: E731
    __complex__ = lambda x: complex(x._get_object())  # noqa: E731
    __int__ = lambda x: int(x._get_object())  # noqa: E731
    __float__ = lambda x: float(x._get_object())  # noqa: E731
    __oct__ = lambda x: oct(x._get_object())  # noqa: E731
    __hex__ = lambda x: hex(x._get_object())  # noqa: E731
    __index__ = lambda x: x._get_object().__index__()  # noqa: E731
    __coerce__ = lambda x, o: x._get_object().__coerce__(x, o)  # noqa: E731
    __enter__ = lambda x: x._get_object().__enter__()  # noqa: E731
    __exit__ = lambda x, *a, **kw: x._get_object().__exit__(*a, **kw)  # noqa: E731
    __radd__ = lambda x, o: o + x._get_object()  # noqa: E731
    __rsub__ = lambda x, o: o - x._get_object()  # noqa: E731
    __rmul__ = lambda x, o: o * x._get_object()  # noqa: E731
    __rdiv__ = lambda x, o: o / x._get_object()  # noqa: E731
    __rtruediv__ = __rdiv__
    __rfloordiv__ = lambda x, o: o // x._get_object()  # noqa: E731
    __rmod__ = lambda x, o: o % x._get_object()  # noqa: E731
    __rdivmod__ = lambda x, o: x._get_object().__rdivmod__(o)  # noqa: E731
    __copy__ = lambda x: copy.copy(x._get_object())  # noqa: E731
    __deepcopy__ = lambda x, memo: copy.deepcopy(x._get_object(), memo)  # noqa: E731

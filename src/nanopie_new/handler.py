from abc import ABC, abstractmethod
from typing import Callable

class Handler():
    """
    """
    def __init__(self):
        """
        """
        self.wraps = None

    def __call__(self, *args, **kwargs):
        """
        """
        if self.wraps:
            return self.wraps(*args, **kwargs)

    def wraps(self, handler: Handler):
        """
        """
        self.wraps = handler

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
        if res:
            return res
        else:
            return super().__call__(*args, **kwargs)

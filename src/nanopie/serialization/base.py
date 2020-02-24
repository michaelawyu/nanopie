from abc import abstractmethod

from ..handler import Handler

class SerializationHandler(Handler):
    """
    """
    def __init__(self, serialization_helper: 'SerializationHelper'):
        """
        """
        self._serialization_helper = serialization_helper

        super().__init__()

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        """
        return super().__call__(*args, **kwargs)

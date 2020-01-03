import json

from ..base import SerializerAbstract
from ...entities.model import Model

class JSONSerializer(SerializerAbstract):
    """
    """
    def serialize(self, entity: Model) -> str:
        """
        """
        raise NotImplementedError

    def deserialize(self, data: str) -> Model:
        """
        """
        raise NotImplementedError
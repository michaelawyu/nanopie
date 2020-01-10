from abc import ABC, abstractmethod
class SerializerAbstract(ABC):
    """
    """

    @abstractmethod
    def serialize(self,
                  value: Union[str, int, float, bool, List, 'Model'],
                  ref: Optional[Union['Field', 'ModelMetaKls']] = None,
                  skip_validation: bool = False) -> str:
        """
        """
        return ''
    
    @abstractmethod
    def deserialize(self,
                    value_str: str,
                    ref: Union['Field', 'ModelMetaKls'],
                    skip_validation: bool = True) -> 'Model':
        """
        """
        return None

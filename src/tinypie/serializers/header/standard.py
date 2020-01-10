from ..base import SerializerAbstract

class URLEncodingQueryStringSerializer(SerializerAbstract):
    """
    """
    def serialize(self,
                  value: Union[str, int, float, bool, List, 'Model'],
                  ref: Optional[Union['Field', 'ModelMetaKls']] = None,
                  skip_validation: bool = False) -> str:
        """
        """
        raise NotImplementedError

    def deserialize(self,
                    value_str: str,
                    ref: Union['Field', 'ModelMetaKls'],
                    skip_validation: bool = True) -> 'Model':
        """
        """
        raise NotImplementedError
from typing import Optional

from .error_bases import ErrorBase

class NoNestedObjectInQueryParametersError(ErrorBase):
    """
    """
    def __init__(self,
                 source: 'QueryParametersMetaKls',
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = 'Nested objects are not supported in query parameters.'
        super.__init__(source=source, message=message)

class NoNestedObjectInHeaderParametersError(ErrorBase):
    """
    """
    def __init__(self,
                 source: 'HeaderParametersMetaKls',
                 message: Optional[str] = None):
        """
        """
        if not message:
            message = 'Nested objects are not supported in header parameters.'
        super.__init__(source=source, message=message)

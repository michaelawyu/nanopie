from typing import Dict

from ..base import HTTPInputParametersAbstract

class FlaskInputParameters(HTTPInputParametersAbstract):
    """
    """
    def __init__(self,
                 request: 'RequestProxy',
                 resource_cls: 'ResourceMetaKls',
                 serializer: 'Serializer'):
        """
        """
        self.request = request
        self.resource_cls = resource_cls
        self.serializer = serializer

    def get_resource(self) -> 'Resource':
        """
        """
        raise NotImplementedError

    def get_query_parameters(self) -> 'QueryParameters':
        """
        """
        raise NotImplementedError

    def get_header_parameters(self) -> 'HeaderParameters':
        """
        """
        raise NotImplementedError

    def get_path_parameters(self) -> Dict:
        """
        """
        raise NotImplementedError
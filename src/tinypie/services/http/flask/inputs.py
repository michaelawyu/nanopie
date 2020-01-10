from ..base import HTTPInputParametersAbstract

class FlaskInputParameters(HTTPInputParametersAbstract):
    """
    """
    def __init__(self,
                 request_proxy: 'LocalProxy',
                 body_serializer: 'SerialzerAbstract',
                 query_str_serializer: 'SerializerAbstract',
                 header_serializer: 'SerializerAbstract'):
        """
        """
        self.request = request_proxy
        self.body_serializer = body_serializer
        self.query_str_serializer = query_str_serializer
        self.header_serializer = header_serializer

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
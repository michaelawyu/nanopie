from typing import Dict

from ..base import HTTPInputParametersAbstract
from ....misc.serialization_errors import (
    InvalidContentTypeError,
    RequestTooLargeError,
)

class FlaskInputParameters(HTTPInputParametersAbstract):
    """
    """
    def __init__(self,
                 request: 'RequestProxy',
                 resource_cls: 'ResourceMetaKls',
                 query_params_cls: 'QueryParametersMetaKls',
                 header_params_cls: 'HeaderParametersMetaKls',
                 serializer: 'Serializer',
                 max_content_length: int):
        """
        """
        self.request = request
        self.resource_cls = resource_cls
        self.query_params_cls = query_params_cls
        self.header_params_cls = header_params_cls
        self.serializer = serializer
        self.max_content_length = max_content_length

    def get_resource(self) -> 'Resource':
        """
        """
        if self.request.content_length and \
           self.request.content_length > self.max_content_length:
            raise RequestTooLargeError(
                max_content_length=self.max_content_length,
                incoming_content_length=self.request.content_length)

        if self.serializer.mime_type != self.request.content_type.lower():
            raise InvalidContentTypeError(
                expected_content_type=self.serializer.mime_type,
                incoming_content_type=self.request.content_type)
        
        data = self.request.get_data()
        return self.serializer.deserialize(data=data, ref=self.resource_cls)

    def get_query_parameters(self) -> 'QueryParameters':
        """
        """
        return self.query_params_cls.parse_from_dict(self.request.args)

    def get_header_parameters(self) -> 'HeaderParameters':
        """
        """
        return self.header_params_cls.parse_from_dict(self.request.headers)

    def get_path_parameters(self) -> Dict:
        """
        """
        return self.request.view_args
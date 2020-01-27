from typing import Dict

from flask import request      

from ..base import APIParams
from ..globals import svc_ctx
from ....misc.serialization_errors import (
    InvalidContentTypeError,
    RequestTooLargeError,
)

class FlaskAPIParams(APIParams):
    """
    """
    def __init__(self,
                 body_params_cls: 'ModelMetaKls',
                 query_params_cls: 'QueryParametersMetaKls',
                 header_params_cls: 'HeaderParametersMetaKls'):
        """
        """
        self.body_params_cls = body_params_cls
        self.query_params_cls = query_params_cls
        self.header_params_cls = header_params_cls

    @property
    def body_params(self) -> 'Resource':
        """
        """
        svc = svc_ctx.svc
        serializer = svc.serializer

        if request.content_length and \
           request.content_length > svc.max_content_length:
            raise NotImplementedError

        if serializer.mime_type != request.content_type.lower():
            raise NotImplementedError
        
        data = request.get_data()
        return serializer.deserialize(data=data, ref=self.body_params_cls)

    @property
    def query_params(self) -> 'QueryParameters':
        """
        """
        return self.query_params_cls.parse_from_dict(request.args)

    @property
    def header_params(self) -> 'HeaderParameters':
        """
        """
        return self.header_params_cls.parse_from_dict(request.headers)

    @property
    def path_params(self) -> Dict:
        """
        """
        return request.view_args
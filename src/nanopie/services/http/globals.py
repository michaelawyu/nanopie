from functools import partial
from typing import Any

from ...globals import look_up_attr
from .proxy import APIParamsProxy, AuthContextProxy, ServiceContextProxy

svc_ctx = ServiceContextProxy(partial(look_up_attr, None, '_svc_ctx'))
api_params = APIParamsProxy(partial(look_up_attr, svc_ctx, 'api_params'))
auth_ctx = AuthContextProxy(partial(look_up_attr, svc_ctx, 'auth_ctx'))

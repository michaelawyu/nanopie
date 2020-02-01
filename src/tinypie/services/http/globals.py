from functools import partial
from typing import Any

from .proxy import APIParamsProxy, ServiceContextProxy

err_msg = ''

def loop_up_attr(ctx: Any, name: str) -> Any:
    """
    """
    v = getattr(ctx, name, None)
    if not v:
        raise RuntimeError(err_msg)
    return v

svc_ctx = ServiceContextProxy(partial(loop_up_attr, None, '_svc_ctx'))
api_params = APIParamsProxy(partial(loop_up_attr, svc_ctx, 'api_params'))
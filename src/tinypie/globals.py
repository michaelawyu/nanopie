from functools import partial
from typing import Any

from .misc import NoContextPresentError
from .proxy import Proxy

def loop_up_ctx(ctx: Any, name: str) -> Any:
    v = getattr(ctx, name, None)
    if not v:
        raise NoContextPresentError
    return v

svc_ctx = Proxy(partial(_loop_up_ctx, None, '_svc_ctx'))
api_params = Proxy(partial(_loop_up_ctx, _svc_ctx, 'api_params'))

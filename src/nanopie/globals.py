from functools import partial
from typing import Any, Dict

from .proxy import GenericProxy

out_of_context_error = "No context is available."
not_set_error = "Specified object is not available yet."


def look_up_attr(ctx: Any, name: str) -> Any:
    """
    """
    v = getattr(ctx, name, None)
    if v == None:
        raise RuntimeError(out_of_context_error)
    return v


def look_up_item(dikt: Dict, name: str) -> Any:
    """
    """
    v = dikt.get(name)
    if v == None:
        raise RuntimeError(not_set_error)
    return v


svc_ctx = GenericProxy(partial(look_up_attr, ctx=None, name="_svc_ctx"))
parsed_request = GenericProxy(
    partial(look_up_item, dikt=svc_ctx, name="parsed_request")
)
svc = GenericProxy(partial(look_up_item, dikt=svc_ctx, name="svc"))
endpoint = GenericProxy(partial(look_up_item, dikt=svc_ctx, name="endpoint"))
request = GenericProxy(partial(look_up_item, dikt=svc_ctx, name="request"))

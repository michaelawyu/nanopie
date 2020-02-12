from functools import partial
from typing import Any

from .proxy import GenericProxy

err_msg = 'Working outside of context.'

def look_up_attr(ctx: Any, name: str) -> Any:
    """
    """
    v = getattr(ctx, name, None)
    if not v:
        raise RuntimeError(err_msg)
    return v

logging_context = GenericProxy(partial(look_up_attr, None, 'logging_context'))
tracing_context = GenericProxy(partial(look_up_attr, None, 'tracing_context'))

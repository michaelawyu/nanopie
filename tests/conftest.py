from functools import partial
from unittest.mock import MagicMock

import pytest

from nanopie.globals import (
    look_up_attr,
    svc_ctx,
    svc,
    endpoint,
    request
)

@pytest.fixture
def setup_ctx():
    ctx_mock = MagicMock()
    ctx_mock._svc_ctx = {
        'parsed_request': MagicMock(name='parsed_request'),
        'svc': MagicMock(name='svc'),
        'endpoint': MagicMock(name='endpoint'),
        'request': MagicMock(name='request')
    }

    svc_ctx.update_proxy_func(partial(look_up_attr, ctx=ctx_mock, name='_svc_ctx'))

from functools import partial

import pytest

from nanopie.globals import (
    look_up_attr,
    look_up_item,
    svc_ctx,
    parsed_request,
    svc,
    endpoint,
    request
)


_svc_ctx = {
    'parsed_request': 'parsed_request',
    'svc': 'svc',
    'endpoint': 'endpoint',
    'request': 'request'
}

class DummyCtx:
    pass

dummy_ctx = DummyCtx()
dummy_ctx._svc_ctx = _svc_ctx

svc_ctx.update_proxy_func(partial(look_up_attr, ctx=dummy_ctx, name='_svc_ctx'))

def test_look_up_attr():
    assert look_up_attr(ctx=dummy_ctx, name='_svc_ctx') == _svc_ctx

    with pytest.raises(RuntimeError) as ex:
        look_up_attr(ctx=dummy_ctx, name='random')
    assert 'No context is available' in str(ex.value)

def test_look_up_item():
    dummy_svc_ctx = {
        'svc': ''
    }
    assert look_up_item(dikt=dummy_svc_ctx, name='svc') == ''

    with pytest.raises(RuntimeError) as ex:
        look_up_item(dikt=dummy_svc_ctx, name='random')
    assert 'Specified object is not available yet.' in str(ex.value)

def test_svc_ctx():
    assert svc_ctx == _svc_ctx

def test_parsed_request():
    assert parsed_request == 'parsed_request'

def test_svc():
    assert svc == 'svc'

def test_endpoint():
    assert endpoint == 'endpoint'

def test_request():
    assert request == 'request'

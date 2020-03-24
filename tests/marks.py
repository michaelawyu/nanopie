import pkgutil

import pytest

from nanopie.auth.creds.jwt import JWT_INSTALLED

jwt_installed = pytest.mark.skipif(not JWT_INSTALLED,
    reason='requires that pyjwt is installed')
cryptography_installed = pytest.mark.skipif(
    pkgutil.find_loader("cryptography") == None,
    reason='requires that cryptography is installed')
pycrypto_installed = pytest.mark.skipif(
    pkgutil.find_loader("Crypto") == None,
    reason='requires that pycrypto is installed')
ecdsa_installed = pytest.mark.skipif(
    pkgutil.find_loader("ecdsa") == None,
    reason='requires that ecdsa is installed')
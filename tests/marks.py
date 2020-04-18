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
fluentd_installed = pytest.mark.skipif(
    pkgutil.find_loader("fluent") == None,
    reason='requires that fluentd is installed'
)
docker_installed = pytest.mark.skipif(
    pkgutil.find_loader("docker") == None,
    reason='requires that docker is installed'
)
stackdriver_installed = pytest.mark.skipif(
    pkgutil.find_loader("google.cloud.logging") == None,
    reason='requires that google-cloud-logging is installed'
)

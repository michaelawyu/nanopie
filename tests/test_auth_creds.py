import pkgutil

import pytest

from nanopie.auth.creds.jwt import JWT_INSTALLED
from nanopie.auth.creds import JWT, JWTValidator
from nanopie.misc.errors import AuthenticationError
from .constants import (
    AUDIENCE,
    ES256_PUBLIC_KEY,
    ES256_TOKEN,
    HS256_SECRET,
    HS256_TOKEN,
    ISSUER,
    RS256_PUBLIC_KEY,
    RS256_TOKEN,
    SIMPLE_TOKEN,
)
from .marks import (
    jwt_installed,
    cryptography_installed,
    pycrypto_installed,
    ecdsa_installed,
)


@pytest.mark.skipif(JWT_INSTALLED, reason="requires that pyjwt is not installed")
def test_jwt_pyjwt_not_installed():
    with pytest.raises(ImportError) as ex:
        jwt = JWT(token="")  # pylint: disable=unused-variable

    assert "pyjwt" in str(ex.value)


@jwt_installed
def test_jwt():
    jwt = JWT(token=SIMPLE_TOKEN)

    assert jwt.header.get("alg") == "HS256"
    assert jwt.header.get("typ") == "JWT"
    assert jwt.payload.get("sub") == "1234567890"
    assert jwt.payload.get("name") == "John Doe"
    assert jwt.payload.get("iat") == 1516239022


@jwt_installed
def test_invalid_jwt():
    with pytest.raises(Exception) as ex:
        jwt = JWT(token="")  # pylint: disable=unused-variable

    assert "The provided JWT is not valid" in str(ex.value)


@pytest.mark.skipif(JWT_INSTALLED, reason="requires that pyjwt is not installed")
def test_jwt_validator_pyjwt_not_installed():
    with pytest.raises(ImportError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="", algorithm=""
        )  # pylint: disable=unused-variable

    assert "pyjwt" in str(ex.value)


@jwt_installed
@pytest.mark.skipif(
    pkgutil.find_loader("cryptography") != None,
    reason="requires that cryptography is not installed",
)
def test_jwt_validator_cryptography_not_installed():
    with pytest.raises(ImportError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="", algorithm=""
        )  # pylint: disable=unused-variable

    assert "cryptography" in str(ex.value)


@jwt_installed
@pytest.mark.skipif(
    pkgutil.find_loader("Crypto") != None,
    reason="requires that pycrypto is not installed",
)
def test_jwt_validator_pycrypto_not_installed():
    with pytest.raises(ImportError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="RS256",
            use_pycrypto=True,
        )

    assert "pycrypto" in str(ex.value)


@jwt_installed
@pytest.mark.skipif(
    pkgutil.find_loader("ecdsa") != None, reason="requires that ecdsa is not installed"
)
def test_jwt_validator_ecdsa_not_installed():
    with pytest.raises(ImportError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="ES256",
            use_ecdsa=True,
        )

    assert "ecdsa" in str(ex.value)


@jwt_installed
@pycrypto_installed
def test_jwt_validator_unsupported_pycrypto_alg():
    with pytest.raises(ValueError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="HS256",
            use_pycrypto=True,
        )

    assert "pycrypto" in str(ex.value)


@jwt_installed
@ecdsa_installed
def test_jwt_validator_unsupported_ecdsa_alg():
    with pytest.raises(ValueError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="HS256",
            use_ecdsa=True,
        )

    assert "ecdsa" in str(ex.value)


@jwt_installed
@cryptography_installed
def test_jwt_validator_options_iss():
    with pytest.raises(ValueError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="HS256",
            verify_iss=True,
        )

    assert "No expected issuer" in str(ex.value)


@jwt_installed
@cryptography_installed
def test_jwt_validator_options_aud():
    with pytest.raises(ValueError) as ex:
        jwt_validator = JWTValidator(
            key_or_secret="",  # pylint: disable=unused-variable
            algorithm="HS256",
            verify_aud=True,
        )

    assert "No expected audience" in str(ex.value)


@jwt_installed
@cryptography_installed
def test_jwt_validator_valid_jwt():
    jwt_validator = JWTValidator(
        key_or_secret=HS256_SECRET,
        algorithm="HS256",
        verify_iss=True,
        issuer=ISSUER,
        verify_aud=True,
        audience=AUDIENCE,
    )

    jwt = JWT(token=HS256_TOKEN)
    jwt_validator.validate(credential=jwt)


@jwt_installed
@cryptography_installed
def test_jwt_validator_invalid_jwt():
    jwt_validator = JWTValidator(
        key_or_secret="my-secret",
        algorithm="HS256",
        verify_iss=True,
        issuer="wrong-issuer",
        verify_aud=True,
        audience=AUDIENCE,
    )

    jwt = JWT(token=HS256_TOKEN)

    with pytest.raises(AuthenticationError) as ex:
        jwt_validator.validate(credential=jwt)

    assert "The provided JWT is not valid (Invalid issuer)" in str(ex.value)


@jwt_installed
@pycrypto_installed
def test_jwt_validator_pycrypto_valid_jwt():
    jwt_validator = JWTValidator(
        key_or_secret=RS256_PUBLIC_KEY,
        algorithm="RS256",
        verify_iss=True,
        issuer=ISSUER,
        verify_aud=True,
        audience=AUDIENCE,
        use_pycrypto=True,
    )

    jwt = JWT(token=RS256_TOKEN)
    jwt_validator.validate(credential=jwt)


@pytest.mark.xfail
@jwt_installed
@ecdsa_installed
def test_jwt_validator_ecdsa_valid_jwt():
    jwt_validator = JWTValidator(
        key_or_secret=ES256_PUBLIC_KEY,
        algorithm="ES256",
        verify_iss=True,
        issuer=ISSUER,
        verify_aud=True,
        audience=AUDIENCE,
        use_ecdsa=True,
    )

    jwt = JWT(token=ES256_TOKEN)
    jwt_validator.validate(credential=jwt)

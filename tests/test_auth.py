from functools import partial
from unittest.mock import MagicMock

import pytest

from nanopie.auth import (
    Credential,
    CredentialValidator,
    AuthenticationHandler,
    HTTPAPIKeyAuthenticationHandler,
    HTTPAPIKeyModes,
    HTTPBasicAuthenticationHandler,
    HTTPOAuth2BearerJWTAuthenticationHandler,
    HTTPOAuth2BearerJWTModes,
)
from nanopie.globals import request
from nanopie.misc.errors import AuthenticationError
from nanopie.services.http.io import HTTPResponse
from .marks import jwt_installed, cryptography_installed
from .constants import ISSUER, RS256_PUBLIC_KEY, RS256_TOKEN

credential = Credential()
credential_extractor = MagicMock(name="credential_extractor")
credential_extractor.extract.return_value = credential
credential_validator = MagicMock(name="credential_validator")
credential_validator.validate.return_value = None


@pytest.fixture
def authentication_handler():
    authentication_handler = AuthenticationHandler(
        credential_extractor=credential_extractor,
        credential_validator=credential_validator,
    )

    return authentication_handler


@pytest.fixture
def http_api_key_authentication_handler_header():
    authentication_handler = HTTPAPIKeyAuthenticationHandler(
        mode=HTTPAPIKeyModes.HEADER,
        key_field_name="api_key",
        credential_validator=credential_validator,
    )

    return authentication_handler


@pytest.fixture
def http_api_key_authentication_handler_query():
    authentication_handler = HTTPAPIKeyAuthenticationHandler(
        mode=HTTPAPIKeyModes.URI_QUERY,
        key_field_name="api_key",
        credential_validator=credential_validator,
    )

    return authentication_handler


@pytest.fixture
def http_basic_authentication_handler():
    authentication_handler = HTTPBasicAuthenticationHandler(
        credential_validator=credential_validator
    )

    return authentication_handler


@pytest.fixture
def http_oauth2_bearer_jwt_authentication_handler_header():
    authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
        key_or_secret=RS256_PUBLIC_KEY,
        algorithm="RS256",
        mode=HTTPOAuth2BearerJWTModes.HEADER,
        verify_iss=True,
        issuer=ISSUER,
    )

    return authentication_handler


@pytest.fixture
def http_oauth2_bearer_jwt_authentication_handler_query():
    authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
        key_or_secret=RS256_PUBLIC_KEY,
        algorithm="RS256",
        mode=HTTPOAuth2BearerJWTModes.URI_QUERY,
        verify_iss=True,
        issuer=ISSUER,
    )

    return authentication_handler


def test_authentication_handler(setup_ctx, authentication_handler):
    assert authentication_handler() == None
    credential_extractor.extract.assert_called_with(request=request)
    credential_validator.validate.assert_called_with(credential=credential)


def test_authentication_handler_before_authentication_failure_not_callable(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:
        authentication_handler.before_authentication(0)
    assert "must decorate a callable" in str(ex.value)


def test_authentication_handler_before_authentication_failure_too_little_params(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.before_authentication
        def before_authentication_multi_params(x):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_before_authentication_failure_too_many_params(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.before_authentication
        def before_authentication_multi_params(
            x, y, z
        ):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_before_authentication_failure_misspelled_param(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.before_authentication
        def before_authentication_wrong_name(x, y):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_before_authentication(
    setup_ctx, authentication_handler
):
    credential_validator_alt = MagicMock(name="credential_validator_alt")
    credential_validator_alt.validate.return_value = None

    @authentication_handler.before_authentication
    def before_authentication(
        auth_handler, credential
    ):  # pylint: disable=unused-variable
        assert auth_handler == authentication_handler
        assert credential == credential
        return credential_validator_alt

    assert authentication_handler() == None
    credential_validator.assert_not_called()
    credential_validator_alt.validate.assert_called_with(credential=credential)


def test_authentication_handler_after_authentication_failure_not_callable(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:
        authentication_handler.after_authentication(0)
    assert "must decorate a callable" in str(ex.value)


def test_authentication_handler_after_authentication_failure_too_little_params(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.after_authentication
        def after_authentication_multi_params(x):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_after_authentication_failure_too_many_params(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.after_authentication
        def after_authentication_multi_params(
            x, y, z
        ):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_after_authentication_failure_misspelled_param(
    setup_ctx, authentication_handler
):
    with pytest.raises(ValueError) as ex:

        @authentication_handler.after_authentication
        def after_authentication_wrong_name(x, y):  # pylint: disable=unused-variable
            pass

    assert (
        "must decorate a callable with two arguments named auth_handler "
        "and credential"
    ) in str(ex.value)


def test_authentication_handler_after_authentication(setup_ctx, authentication_handler):
    flag = MagicMock(return_value=None)

    @authentication_handler.after_authentication
    def after_authentication(
        auth_handler, credential
    ):  # pylint: disable=unused-variable
        assert auth_handler == authentication_handler
        assert credential == credential
        return flag()

    assert authentication_handler() == None
    flag.assert_called()


def test_authentication_handler_http_api_key_header(
    setup_ctx, http_api_key_authentication_handler_header
):
    request.headers = {"api_key": "api-key"}  # pylint: disable=assigning-non-slot

    assert http_api_key_authentication_handler_header() == None
    credential = credential_validator.validate.call_args[1]["credential"]
    assert credential.key == "api-key"


def test_authentication_handler_http_api_key_query(
    setup_ctx, http_api_key_authentication_handler_query
):
    request.query_args = {"api_key": "api-key"}  # pylint: disable=assigning-non-slot

    assert http_api_key_authentication_handler_query() == None


def test_authentication_handler_http_api_key_header_failure_not_HTTP_request(
    setup_ctx, http_api_key_authentication_handler_header
):
    with pytest.raises(AttributeError) as ex:
        http_api_key_authentication_handler_header()

    assert "not a valid HTTP request" in str(ex.value)


def test_authentication_handler_http_api_key_header_failture_no_header(
    setup_ctx, http_api_key_authentication_handler_header
):
    request.headers = {}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_api_key_authentication_handler_header()

    assert "does not have an API key" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


def test_authentication_handler_http_api_key_query_failure_not_HTTP_request(
    setup_ctx, http_api_key_authentication_handler_query
):
    with pytest.raises(AttributeError) as ex:
        http_api_key_authentication_handler_query()

    assert "not a valid HTTP request" in str(ex.value)


def test_authentication_handler_http_api_key_query_failture_no_query_arg(
    setup_ctx, http_api_key_authentication_handler_query
):
    request.query_args = {}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_api_key_authentication_handler_query()

    assert "does not have an API key" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


def test_authentication_handler_http_basic(
    setup_ctx, http_basic_authentication_handler
):
    request.headers = {  # pylint: disable=assigning-non-slot
        "Authorization": "Basic dGVzdDoxMjPCow=="
    }

    assert http_basic_authentication_handler() == None
    credential = credential_validator.validate.call_args[1]["credential"]
    assert credential.username == "test"
    assert credential.password == "123£"


def test_authentication_handler_http_basic_failure_not_HTTP_request(
    setup_ctx, http_basic_authentication_handler
):
    with pytest.raises(AttributeError) as ex:
        http_basic_authentication_handler()

    assert "not a valid HTTP request" in str(ex.value)


def test_authentication_handler_http_basic_failure_no_header(
    setup_ctx, http_basic_authentication_handler
):
    request.headers = {}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_basic_authentication_handler()

    assert "does not have an HTTP Authorization request header" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {"WWW-Authenticate": "Basic"}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


def test_authentication_handler_http_basic_failure_wrong_type(
    setup_ctx, http_basic_authentication_handler
):
    request.headers = {"Authorization": "Bearer"}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_basic_authentication_handler()

    assert (
        "does not have an HTTP Authorization request header with the Basic type"
        in str(ex.value)
    )
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {"WWW-Authenticate": "Basic"}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


def test_authentication_handler_http_basic_failure_corrupted_credential(
    setup_ctx, http_basic_authentication_handler
):
    request.headers = {  # pylint: disable=assigning-non-slot
        "Authorization": "Basic $ab123"
    }

    with pytest.raises(AuthenticationError) as ex:
        http_basic_authentication_handler()

    assert "Cannot decode the credential data" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 403
    assert ex.value.response.headers == {"WWW-Authenticate": "Basic"}
    assert ex.value.response.mime_type == "text/html"
    assert "403 Forbidden" in ex.value.response.data


def test_authentication_handler_http_basic_failure_malformed_credential(
    setup_ctx, http_basic_authentication_handler
):
    request.headers = {  # pylint: disable=assigning-non-slot
        "Authorization": "Basic dGVzdA=="
    }

    with pytest.raises(AuthenticationError) as ex:
        http_basic_authentication_handler()

    assert "malformed" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 403
    assert ex.value.response.headers == {"WWW-Authenticate": "Basic"}
    assert ex.value.response.mime_type == "text/html"
    assert "403 Forbidden" in ex.value.response.data


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_header(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_header
):
    request.headers = {  # pylint: disable=assigning-non-slot
        "Authorization": "Bearer" + " " + RS256_TOKEN
    }

    assert http_oauth2_bearer_jwt_authentication_handler_header() == None


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_header_failure_not_HTTP_request(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_header
):
    with pytest.raises(AttributeError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_header()

    assert "not a valid HTTP request" in str(ex.value)


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_header_failure_no_header(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_header
):
    request.headers = {}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_header()

    assert "does not have an HTTP Authorization request header" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {"WWW-Authenticate": "Bearer"}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_header_failure_wrong_type(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_header
):
    request.headers = {"Authorization": "Basic"}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_header()

    assert (
        "does not have an HTTP Authorization request header with the Bearer type"
        in str(ex.value)
    )
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {"WWW-Authenticate": "Bearer"}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_header_failure_invalid_JWT(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_header
):
    request.headers = {  # pylint: disable=assigning-non-slot
        "Authorization": "Bearer $ab123"
    }

    with pytest.raises(AuthenticationError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_header()

    assert "JWT is not valid" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 403
    assert ex.value.response.headers == {
        "WWW-Authenticate": "Bearer error=invalid_token"
    }
    assert ex.value.response.mime_type == "text/html"
    assert "403 Forbidden" in ex.value.response.data


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_query(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_query
):
    request.query_args = {  # pylint: disable=assigning-non-slot
        "access_token": RS256_TOKEN
    }

    assert http_oauth2_bearer_jwt_authentication_handler_query() == None


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_query_failure_not_HTTP_request(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_query
):
    with pytest.raises(AttributeError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_query()

    assert "not a valid HTTP request" in str(ex.value)


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_query_failure_no_query_arg(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_query
):
    request.query_args = {}  # pylint: disable=assigning-non-slot

    with pytest.raises(AuthenticationError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_query()

    assert "does not have an access_token argument" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 401
    assert ex.value.response.headers == {"WWW-Authenticate": "Bearer"}
    assert ex.value.response.mime_type == "text/html"
    assert "401 Unauthorized" in ex.value.response.data


@jwt_installed
@cryptography_installed
def test_authentication_handler_http_oauth2_bearer_jwt_query_failure_invalid_JWT(
    setup_ctx, http_oauth2_bearer_jwt_authentication_handler_query
):
    request.query_args = {  # pylint: disable=assigning-non-slot
        "access_token": "$ab123"
    }

    with pytest.raises(AuthenticationError) as ex:
        http_oauth2_bearer_jwt_authentication_handler_query()

    assert "JWT is not valid" in str(ex.value)
    assert isinstance(ex.value.response, HTTPResponse)
    assert ex.value.response.status_code == 403
    assert ex.value.response.headers == {
        "WWW-Authenticate": "Bearer error=invalid_token"
    }
    assert ex.value.response.mime_type == "text/html"
    assert "403 Forbidden" in ex.value.response.data

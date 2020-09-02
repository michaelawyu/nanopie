# Authentication

As introduced in [Overview](/overview), nanopie provides pluggable solutions
for authentication, in the form of authentication handlers. When added to 
an endpoint or a service, these handlers validate incoming requests
automatically.

The validation of requests is based on the credentials that come
with the requests, such as API keys, user credentials, and bearer JWTs.
An authentication handler first extracts credentials from requests using
a credential extractor, then validate them using a credential validator.
Depending on the authentication scheme you use, some authentication handlers
have preconfigured credential extractors and validators, while others may
need custom ones. In addition, authentication handlers provide the
`before_authentication` and `after_authentication` functions,
which allows you to configure how handlers validate requests at runtime; for
example, you may rotate the key used for credential signature verification
for certain credentials, or perform some additional, custom checks on
credentials that are not supported yet in the handlers.

At this moment, nanopie provides the following authentication handlers:

Service Type  | Authentication Scheme | Authentication Handler
------------- | --------------------- | ----------------------
HTTP | API keys | `HTTPAPIKeyAuthenticationHandler`
HTTP | [HTTP Basic (RFC6717)](https://tools.ietf.org/html/rfc7617) | `HTTPAPIKeyAuthenticationHandler`
HTTP | [HTTP OAuth2 Bearer Token (RFC 6750)](https://tools.ietf.org/html/rfc6750) + [JWT (RFC 7519)](https://tools.ietf.org/html/rfc7519) | `HTTPOAuthBearerJWTAuthenticationHandler`

## Using authentication handlers

### Authentication handlers for HTTP services

#### Authentication with API keys

To authenticate requests in your HTTP microservices/API backends with API
keys, add an `HTTPAPIKeyAuthenticationHandler` to your service. To use this
authentication handler, you must specify where the API keys reside, and
provide it with a credential validator that validates the API key.

To create a credential validator, inherit from the `CredentialValidator` class
and override the `validate` method, which takes a `Key` credential as input:

``` python
from nanopie import CredentialValidator
from nanopie.misc.errors import AuthenticationError
from nanopie.auth.http_api_key import INVALID_KEY_RESPONSE

class KeyCredentialValidator(CredentialValidator):
    def validate(self, credential):
        # The `Key` credential has only one attribute, `key`, which is the
        # API key included in the request
        if is_correct(credential.key):
            pass
        else:
            # Raise an AuthenticationError with an HTTP response when the
            # authentication fails; nanopie will return the attached response
            # to the client
            raise AuthenticationError(
                "The API key is not correct.",
                response=INVALID_KEY_RESPONSE)

credential_validator = KeyCredentialValidator()
```

!!! note
    See [Exceptions](/exceptions)
    for instructions on how to customize the response authentication handlers
    return to clients when an error occurs.

Next, add the credential validator to the HTTP API key authentication handler.
If your API key resides in the HTTP headers with the name `api_key`, create an
`HTTPAPIKeyAuthenticationHandler` with the `mode` set to `HEADER` and the
`key_field_name` to `api_key`; on the other hand, if your API key resides
in the URI query arguments with the same name, use the `mode` `URI_QUERY`
instead.

``` python
from nanopie import HTTPAPIKeyAuthenticationHandler

authentication_handler = HTTPAPIKeyAuthenticationHandler(
    mode="HEADER",
    key_field_name="api_key",
    # The credential validator you just created
    credential_validator=credential_validator
)
```

!!! note
    The available modes are listed in `nanopie.HTTPAPIKeyModes`. Instead of
    the raw values, you may also use `HTTPAPIKeyModes.HEADER` and
    `HTTPAPIKeyModes.URI_QUERY`.

Finally, add the authentication to your endpoint or service. For instructions,
see [Services](/services); the code snippet below showcases how to add
an authentication handler to a Flask microservice:

``` python
from nanopie import FlaskService

app = Flase(__name__)
svc = FlaskService(app=app,
                   # The authentication handler you just created
                   authn_hanlder=authentication_handler)
```

#### Authentication with HTTP Basic scheme

To authenticate requests in your HTTP microservices/API backends with the
HTTP Basic scheme, add an `HTTPBasicAuthenticationHandler` to your service.
To use this authentication handler, you must provide it with a
credential validator that validates the user credentials that comes
with the requests.

To create a credential validator, inherit from the `CredentialValidator` class
and override the `validate` method, which takes a `UserCredential`
credential as input:

``` python
from nanopie import CredentialValidator
from nanopie.auth.http_basic import INVALID_CREDENTIAL_RESPONSE

class UserCredentialValidator(CredentialValidator):
    def validate(self, credential):
        # The `UserCredential` credential has two attributes,
        # `username` and `password`, which are extracted from the Auth header
        # in the HTTP request; nanopie performs Base64 decoding on them
        # automatically
        if is_correct(credential.username, credential.password):
            pass
        else:
            # Raise an AuthenticationError with an HTTP response when the
            # authentication fails; nanopie will return the attached response
            # to the client
            raise AuthenticationError(
                "The API key is not correct.",
                response=INVALID_CREDENTIAL_RESPONSE)

credential_validator = UserCredentialValidator()
```

!!! note
    See [Exceptions](/exceptions)
    for instructions on how to customize the response authentication handlers
    return to clients when an error occurs.

Next, add the credential validator to the HTTP Basic authentication handler:

``` python
from nanopie import HTTPBasicAuthenticationHandler

authentication_handler = HTTPBasicAuthenticationHandler(
    # The credential validator you just created
    credential_validator=credential_validator
)
```

Finally, add the authentication to your endpoint or service. For instructions,
see [Services](/services); the code snippet below showcases how to add
an authentication handler to a Flask microservice:

``` python
from nanopie import FlaskService

app = Flase(__name__)
svc = FlaskService(app=app,
                   # The authentication handler you just created
                   authn_hanlder=authentication_handler)
```

#### Authentication with HTTP OAuth2 Bearer Token scheme and JWTs

To authenticate requests in your HTTP microservices/API backend with the
HTTP OAuth2 Bearer Token + JWT scheme, add an
`HTTPOAuth2BearerJWTAuthenticationHandler` to your service. This
authentication handler is capable of extracting and validating credentials
(JWTs) by itself; all you need to do is to specify where the bearer token
resides, plus the algorithm and key or secret used to sign JWTs.

!!! note
    This authentication handler supports the following algorithms:

    - `HS256`, `HS384`, or `HS512` (HMAC with SHA-256/SHA-384/SHA-512)
    - `RS256`, `RS384`, or `RS512` (RSA with SHA-256/SHA-384/SHA-512)
    - `ES256`, `ES384`, or `ES512` (ECDSA with SHA-256/SHA-384/SHA-512)
    - `PS256`, `PS384`, or `PS512` (PSS with SHA-256/SHA-384/SHA-512)

As specified in [RFC 6750](https://tools.ietf.org/html/rfc6750), nanopie
supports extraction of bearer tokens from two places: the headers of HTTP
requests, or the URI query arguments of HTTP requests. If the former is true,
create an `HTTPOAuth2BearerJWTAuthenticator` with the `mode` set to `HEADER`;
this is also default mode `HTTPOAuth2BearerJWTAuthenticator` will use.
Otherwise, set the `mode` to `URI_QUERY`.

``` python
from nanopie import HTTPOAuth2BearerJWTAuthenticationHandler

authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    mode="HEADER",
    key_or_secret="YOUR-KEY-OR-SECRET",
    algorithm="YOUR-ALGORITHM"
)
```

!!! note
    The available modes are listed in `nanopie.HTTPOAuth2BearerJWTModes`.
    Instead of the raw values, you may also use
    `HTTPOAuth2BearerJWTModes.HEADER` and
    `HTTPOAuth2BearerJWTModes.URI_QUERY`.

Next, add the authentication to your endpoint or service. For instructions,
see [Services](/services); the code snippet below showcases how to add
an authentication handler to a Flask microservice:

``` python
from nanopie import FlaskService

app = Flase(__name__)
svc = FlaskService(app=app,
                   # The authentication handler you just created
                   authn_hanlder=authentication_handler)
```

Note that this authentication handler also provides a number of options
that allows you to fine-tune the verification of JWTs: you may specify
the following keyword arguments when initializing the handler:

Option  | Description
------------- | -------------
`use_pycrypto` | If set to `True`, use the `pycrypto` package for encryption/decryption instead of the default `cryptography` package. This package only supports RS algorithms.
`use_ecdsa` | If set to `True`, use the `ecdsa` package for encryption/decryption instead of the default `cryptography` package. This package only supports ES algorithms.
`verify_signature` | If set to `False`, the JWT signature will not be validated. Defaults to `True`.
`verify_exp`  | If set to `False`, the `exp` (expiration) claim of the JWT (if any) will not be validated. Defaults to `True`.
`verify_nbf`  | If set to `False`, the `nbf` (not before) claim of the JWT (if any) will not be validated. Defaults to `True`.
`verify_iat` | If set to `False`, the `iat` (issued at) claim of the JWT (if any) will not be validated. Defaults to `True`.
`verify_aud` | If set to `True`, the `aud` (audience) claim of the JWT will be validated. Defaults to `False`.
`verify_iss` | If set to `True`, the `iss` (issuer) claim of the JWT will be validated. Defaults to `False`.
`require_exp` | If set to `True`, the `exp` (expiration) claim must be present in the JWT. Defaults to `False`.
`require_iat` | If set to `True`, the `iat` (issued at) claim must be present in the JWT. Defaults to `False`.
`require_nbf` | If set to `True`, the `nbf` (not before) claim must be present in the JWT. Defaults to `False`.
`audience` | The expected audience of the JWT.
`issuer` | The expected issuer of the JWT.
`leeway` | The margin of error for the `exp` (expiration) claim. Defaults to `0`.

The instructions so far use a static configuration for JWT verification; in
production environments, it is often required to verify JWTs dynamically, i.e.
using different algorithms and key/secrets for different JWTs. It is also
common for developers to inspect additional, custom fields in the JWT for
further security checks. Both use cases can be
achieved in nanopie using the `before_authentication` and `after_authentication`
methods; see the section below for more information.

### `before_authentication` and `after_authentication` functions

Authentication handlers in nanopie includes two additional decorator methods,
`before_authentication` and `after_authentication`, which allows developers
to perform operations before and after the actual authentication workflow.

`before_authentication` decorates a method that is invoked before the
credential is verified but after the credential is extracted. The method
must accept exactly two arguments, which are:

* `auth_handler`: The running authentication handler
* `credential`: The credential extracted (but not verified yet)

And this method should return `None` or a credential validator. If the latter
is the case, the running authentication handler will use the returned
credential validator, instead of the one specified at the time of compilation,
to validate credentials.

`before_authentication` is perfect for setting up dynamic credential validation.
The code snippet below, for example, configures an
`HTTPOAuth2BearerJWTAuthenticator` to verify JWTs using the algorithm
and public key claimed within the JWTs themselves:

``` python
from nanopie import HTTPOAuth2BearerJWTAuthenticationHandler
# This is the class of the default JWT validator in the HTTP OAuth2 Bearer
# Token w/ JWT authentication handler
from nanopie.auth.http_oauth2_bearer_jwt import HTTPOAuth2BearerJWTValidator

authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    mode="HEADER",
    key_or_secret="DEFAULT-KEY-OR-SECRET",
    algorithm="DEFAULT-ALGORITHM"
)

@authentication_handler.before_authentication
def before_authentication(self, auth_handler, credential):
    algorithm = credential.headers.get('algorithm')
    public_key = credential.headers.get('public_key')

    # Use the default algorithm and key if the JWT does not specify them
    if not algorithm:
        algorithm = auth_handler.alg
    if not public_key:
        public_key = auth_handler.pk
    
    # This is the options used for fine tuning JWT verification
    kwargs = auth_handler.kwargs
    
    return HTTPOAuth2BearerJWTValidator(key_or_secret=key_or_secret,
                                        algorithm=algorithm,
                                        **kwargs)
```

`after_authentication`, on the other hand, decorates a method that is invoked
after the credential is verified. This method also accepts the two arguments
listed earlier and should always return `None`.

`after_authentication` is perfect for setting up additional checks on
credentials. The code snippet below, for example, configures an
`HTTPOAuth2BearerJWTAuthenticator` to verify a custom claim in the JWT
payload:

``` python
from nanopie import HTTPOAuth2BearerJWTAuthenticationHandler
from nanopie.misc.errors import AuthenticationError
from nanopie.auth.http_oauth2_bearer_jwt import INVALID_TOKEN_RESPONSE

authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    mode="HEADER",
    key_or_secret="DEFAULT-KEY-OR-SECRET",
    algorithm="DEFAULT-ALGORITHM"
)

@authentication_handler.after_authentication
def after_authentication(self, auth_handler, credential):
    custom_claim = credential.payload.get('custom')

    if not custom_claim or not is_correct(custom_claim):
        raise AuthenticationError("The custom claim is not correct",
                                  response=INVALID_TOKEN_RESPONSE)

```

!!! note
    See [Exceptions](/exceptions)
    for instructions on how to customize the response authentication handlers
    return to clients when an error occurs.

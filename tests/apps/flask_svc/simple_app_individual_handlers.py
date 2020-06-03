from flask import Flask
from nanopie import (
    FlaskService,
    LoggingHandler,
    HTTPAPIKeyAuthenticationHandler,
    HTTPAPIKeyModes,
    CredentialValidator,
    HTTPBasicAuthenticationHandler,
    HTTPOAuth2BearerJWTAuthenticationHandler,
    OpenTelemetryTracingHandler,
    request,
    parsed_request,
)
from nanopie.misc.errors import ValidationError

if __package__ == None or __package__ == "":
    from constants import ES256_PUBLIC_KEY  # pylint: disable=no-name-in-module
    from models import User, UpdateUserRequest, ListUsersQueryArgs, VerifyUserHeaders
    from simple_app import (
        dummy_storage,
        get_user,
        create_user,
        update_user,
        delete_user,
        list_users,
        find_user_data,
        USER_NOT_EXIST_RES,
        INVALID_INPUT_RES,
    )
else:
    from .constants import ES256_PUBLIC_KEY
    from .models import User, UpdateUserRequest, ListUsersQueryArgs, VerifyUserHeaders
    from .simple_app import (
        dummy_storage,
        get_user,
        create_user,
        update_user,
        delete_user,
        list_users,
        find_user_data,
        USER_NOT_EXIST_RES,
        INVALID_INPUT_RES,
    )

app = Flask(__name__)
micro_svc = FlaskService(app=app)

oauth2_auth_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    key_or_secret=ES256_PUBLIC_KEY, algorithm="ES256"
)


class CustomAPIKeyCredentialValidator(CredentialValidator):
    def validate(self, credential):
        assert credential.key == "123"


api_key_auth_handler = HTTPAPIKeyAuthenticationHandler(
    mode=HTTPAPIKeyModes.URI_QUERY,
    key_field_name="api_key",
    credential_validator=CustomAPIKeyCredentialValidator(),
)


class CustomBasicCredentialValidator(CredentialValidator):
    def validate(self, credential):
        assert credential.username == "aladdin"
        assert credential.password == "opensesame"


basic_auth_handler = HTTPBasicAuthenticationHandler(
    credential_validator=CustomBasicCredentialValidator()
)

logging_handler_get_user = LoggingHandler(
    default_logger_name="get_user_logger", span_name="get_user_logging"
)
tracing_handler_get_user = OpenTelemetryTracingHandler(
    with_span_name="get_user_tracing"
)
micro_svc.add_get_endpoint(
    name="get_user",
    rule="/users/<int:uid>",
    func=get_user,
    authn_handler=oauth2_auth_handler,
    logging_handler=logging_handler_get_user,
    tracing_handler=tracing_handler_get_user,
)

logging_handler_create_user = LoggingHandler(
    default_logger_name="create_user_logger", span_name="create_user_logging"
)
tracing_handler_create_user = OpenTelemetryTracingHandler(
    with_span_name="create_user_tracing"
)
micro_svc.add_create_endpoint(
    name="create_user",
    rule="/users",
    func=create_user,
    data_cls=User,
    authn_handler=oauth2_auth_handler,
    logging_handler=logging_handler_create_user,
    tracing_handler=tracing_handler_create_user,
)

logging_handler_update_user = LoggingHandler(
    default_logger_name="update_user_logger", span_name="update_user_logging"
)
tracing_handler_update_user = OpenTelemetryTracingHandler(
    with_span_name="update_user_tracing"
)
micro_svc.add_update_endpoint(
    name="update_user",
    rule="/users/<int:uid>",
    func=update_user,
    data_cls=UpdateUserRequest,
    authn_handler=api_key_auth_handler,
    logging_handler=logging_handler_update_user,
    tracing_handler=tracing_handler_update_user,
)

logging_handler_delete_user = LoggingHandler(
    default_logger_name="delete_user_logger", span_name="delete_user_logging"
)
tracing_handler_delete_user = OpenTelemetryTracingHandler(
    with_span_name="delete_user_tracing"
)
micro_svc.add_delete_endpoint(
    name="delete_user",
    rule="/users/<int:uid>",
    func=delete_user,
    authn_handler=api_key_auth_handler,
    logging_handler=logging_handler_delete_user,
    tracing_handler=tracing_handler_delete_user,
)

logging_handler_list_users = LoggingHandler(
    default_logger_name="list_users_logger", span_name="list_users_logging"
)
tracing_handler_list_users = OpenTelemetryTracingHandler(
    with_span_name="list_users_tracing"
)
micro_svc.add_list_endpoint(
    name="list_users",
    rule="/users",
    func=list_users,
    query_args_cls=ListUsersQueryArgs,
    authn_handler=basic_auth_handler,
    logging_handler=logging_handler_list_users,
    tracing_handler=tracing_handler_list_users,
)

logging_handler_verify_user = LoggingHandler(
    default_logger_name="verify_user_logger", span_name="verify_user_logging"
)
tracing_handler_verify_user = OpenTelemetryTracingHandler(
    with_span_name="verify_user_tracing"
)


@micro_svc.custom(
    name="verify_user",
    rule="/users/<int:uid>",
    verb="verify",
    method="GET",
    headers_cls=VerifyUserHeaders,
    authn_handler=basic_auth_handler,
    logging_handler=logging_handler_verify_user,
    tracing_handler=tracing_handler_verify_user,
)
def verify_user(uid):
    i, user_data = find_user_data(uid)  # pylint: disable=unused-variable
    if user_data == None:
        return USER_NOT_EXIST_RES

    verify_user_headers = parsed_request.headers
    try:
        verify_user_headers.validate()
    except ValidationError:
        return INVALID_INPUT_RES

    assert verify_user_headers.test == "A test"
    assert verify_user_headers.another_test == 4

    user = User.from_dikt(user_data)
    return user


if __name__ == "__main__":
    app.run(debug=True)

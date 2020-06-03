from flask import Flask
from nanopie import (
    FlaskService,
    LoggingHandler,
    HTTPOAuth2BearerJWTAuthenticationHandler,
    OpenTelemetryTracingHandler,
)

if __package__ == None or __package__ == "":
    from constants import ES256_PUBLIC_KEY  # pylint: disable=no-name-in-module
    from models import User, UpdateUserRequest, ListUsersQueryArgs
    from simple_app import (
        dummy_storage,
        get_user,
        create_user,
        update_user,
        delete_user,
        list_users,
        verify_user,
    )
else:
    from .constants import ES256_PUBLIC_KEY
    from .models import User, UpdateUserRequest, ListUsersQueryArgs
    from .simple_app import (
        dummy_storage,
        get_user,
        create_user,
        update_user,
        delete_user,
        list_users,
        verify_user,
    )

auth_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    key_or_secret=ES256_PUBLIC_KEY, algorithm="ES256"
)
logging_handler = LoggingHandler()
tracing_handler = OpenTelemetryTracingHandler()

app = Flask(__name__)
micro_svc = FlaskService(
    app=app,
    authn_handler=auth_handler,
    logging_handler=logging_handler,
    tracing_handler=tracing_handler,
)

micro_svc.add_get_endpoint(name="get_user", rule="/users/<int:uid>", func=get_user)

micro_svc.add_create_endpoint(
    name="create_user", rule="/users", data_cls=User, func=create_user
)

micro_svc.add_update_endpoint(
    name="update_user",
    rule="/users/<int:uid>",
    data_cls=UpdateUserRequest,
    func=update_user,
)

micro_svc.add_delete_endpoint(
    name="delete_user", rule="/users/<int:uid>", func=delete_user
)

micro_svc.add_list_endpoint(
    name="list_users", rule="/users", func=list_users, query_args_cls=ListUsersQueryArgs
)

micro_svc.add_custom_endpoint(
    name="verify_user",
    rule="/users/<int:uid>",
    verb="verify",
    method="GET",
    func=verify_user,
)

if __name__ == "__main__":
    app.run(debug=True)

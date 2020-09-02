from flask import Flask
from nanopie import (
    FlaskService,
    HTTPOAuth2BearerJWTModes,
    HTTPOAuth2BearerJWTAuthenticationHandler,
    LoggingHandler,
    OpenTelemetryTracingHandler,
)

# Import the User model created in the last step
from user import User

# Create a Flask app
app = Flask(__name__)

# Create an authentication handler
authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    # The secret used for generating JWT tokens
    key_or_secret="my-secret",
    # The algorithm used for generating JWT tokens
    algorithm="HS256",
    # Specify that the token comes in the URI query string of the HTTP request
    mode=HTTPOAuth2BearerJWTModes.URI_QUERY,
)

# Create a logging handler and a tracing handler.
logging_handler = LoggingHandler()
tracing_handler = OpenTelemetryTracingHandler()

# Create a nanopie microservice with an authentication handler,
# a logging handler, and a tracing handler.
svc = FlaskService(
    app=app,
    authn_handler=authentication_handler,
    logging_handler=logging_handler,
    tracing_handler=tracing_handler,
)

# Create a HTTP RESTful API endpoint with the `GET` HTTP method
@svc.get(name="get_user", rule="/users/<int:uid>")
def get_user(uid):
    # Always return the same user regardless of the ID provided
    return User(name="Albert Wesker", age=49)


if __name__ == "__main__":
    app.run(debug=True, port=8080)

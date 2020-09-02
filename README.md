# nanopie

## Overview

nanopie is a lightweight Python framework for writing microservices and API
backends. The framework provides pluggable solutions for a number of tasks,
such as input validation, serialization/deserialization, authentication,
logging, and tracing, commonly encountered in microservice and API backend
development.

**Note**: nanopie in still in Development. At this moment, nanopie supports
only HTTP (RESTful) microservices/API backends.

## Features

* **Bring your own transport**

    Python has a large number of web framework + server solutions, such
    [flask](https://flask.palletsprojects.com/en/1.1.x/) +
    [gunicorn](http://www.gunicorn.org/),
    [quart](https://pgjones.gitlab.io/quart/) + 
    [uvicorn](https://www.uvicorn.org/),
    and [Tornado](http://www.tornadoweb.org/); many of these options are
    mature, time-tested, and widely-adopted, and it is not nanopie's design
    goal to create another system for processing requests. Instead, nanopie
    leaves the request processing part up to a transport of your choice.
    This allows developers to use nanopie with any web framework and
    server they are most familiar with; it is also possible to
    switch transports at will as you see fit without having to drastically
    change the code.

* **Data modeling and validation**

    nanopie provides a data modeling mechansim, based on metaclasses
    in Python ([PEP 3115](https://www.python.org/dev/peps/pep-3115/)),
    that helps developers model the inputs and outputs to the endpoints of
    their microservices and API backends, making it easy to access data
    idiomatically. nanopie models also features automatic data validation,
    saving the trouble of writing additional checking logic in the code.

    ``` python
    from nanopie import Model, IntField, StringField

    class User(Model):
        name = StringField(max_length=20, min_length=1, pattern="[a-zA-Z]*")
        age = IntField(maximum=100, minimum=0)

    user = User(name="Albert Wesker", age=49)
    print(user.name)
    print(user.age)

    # This will raise an exception
    user = User(name="Link in BotW", age=117)
    ```

    In addition, nanopie models work seamlessly with the built-in
    serialization/deserialization solution; once configured, nanopie
    can automatically parse incoming requests into data model objects,
    and return data model objects as responses in interchangable formats.

* **Pluggable authentication, serialization, logging, and tracing solutions**

    nanopie provides a number of solutions for common tasks in microservices and
    API backend development, known as handlers. You can add handlers to the
    endpoints of your microservices and API backends so that they can perform
    the tasks when requests arrive at the endpoint:
    `HTTPBasicAuthenticationHandler`, for example, authenticates requests
    based on the `Basic` HTTP Authentication Scheme
    ([RFC 7617](https://tools.ietf.org/html/rfc7617)),
    and `OpenTelemetryTracingHandler`, for another example, traces the execution
    of your endpoint and writes the trace to `STDOUT/STDERR` every time a
    request is being processed.

    Handlers can be chained together to execute a sequence of actions.
    A typically pattern is to chain an authentication handler,
    a logging handler, a tracing handler, a serialization handler together
    for an endpoint, so that when a request arrives at the endpoint,
    it is authenticated, logged, and traced by respective handlers, with its
    payload deserialized into an object of nanopie data model automatically.

    ![Handlers](https://github.com/michaelawyu/nanopie/blob/master/docs/images/handlers_alt.png?raw=true)

## Installation

To install nanopie, run the following command:

``` sh
pip install nanopie
```

## Getting started

The following example showcases how to use nanopie to write a simple
microservice with RESTful HTTP API for user management with one
endpoint, `get_user`, which returns a user with a specific user ID.

### Setup

Install `nanopie` and `flask`, a popular Python web micro-framework in your
project. A `Flask` app will serve as the transport of your `nanopie`
microservice in this example:

``` sh
pip install nanopie flask
```

### Defining the data model

The microservice you will build in this example, as introduced at the beginning
of this section, has only one endpoint, which returns the information of
a specific user to clients. To model the user information, create a `user.py`
script in your project with the following `nanopie` data model:

``` python
from nanopie import (
    Model,
    IntField,
    StringField
)

class User(Model):
    name = StringField(max_length=20, min_length=1, pattern="[a-zA-Z]*")
    age = IntField(maximum=100, minimum=0)
```

The `User` model includes two fields, `name`, and `age`, which takes a
`String` value and a `Integer` value respectively. 

Note that both fields have hints and constraints specified:
    
* The `name` field must be an alphabetic string with a maximum of 20
characters and a minimum of 1 character.
* The `age` field must be an integer no smaller than `1` and no greater
than `100`.

`nanopie` can use these hints and constraints to validate data.

### Writing the microservice

Create a Python script, `main.py`, as follows in your project. The script
first creates a Flask app, then creates a `FlaskService` object that nanopie
provides for using a Flask app as the transport of your microservice. The
`FlaskService` object includes a number of methods (decorators) for specifying
HTTP microservice or API backend endpoints; in the case of this project, you
will create a `GET` endpoint which returns a `User` object as defined by
the `User` model detailed in the previous section.

``` python
from flask import Flask
from nanopie import (
    FlaskService
)

# Import the User model created in the last step
from user import User

# Create a Flask app
app = Flask(__name__)
# Create a nanopie microservice with the Flask app as transport
svc = FlaskService(app=app)

# Create a HTTP RESTful API endpoint with the `GET` HTTP method
@svc.get(name="get_user", rule="/users/<int:uid>")
def get_user(uid):
    # Always return the same user regardless of the ID provided
    return User(name="Albert Wesker", age=49)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
```

Run the script:

``` sh
python main.py
```

Open the browser of your system and visit `127.0.0.1:8080/users/1`. It should
return the following JSON string:

``` json
{"name": "Albert Wesker", "age": 49}
```

### Adding authentication capabilities

At this moment your microservice accepts any request from the network. To
protect data from unauthorized sources, you should authenticate
requests in the microservice. nanopie provides a number of pluggable
authentication solutions, known as authentication handlers, that perform
the authentication of requests automatically; for this project, you will
enable HTTP OAuth2 Bearer Token with JWT ([RFC 6750](https://tools.ietf.org/html/rfc6750),
[RFC 7519](https://tools.ietf.org/html/rfc7519)) based authentication in the
service using the
authentication handler `HTTPOAuth2BearerJWTAuthenticationHandler`.

To enable authentication, edit `main.py` and create
a `HTTPOAuth2BearerJWTAuthenticationHandler`:

``` python
from flask import Flask
from nanopie import (
    FlaskService,
    HTTPOAuth2BearerJWTModes,
    HTTPOAuth2BearerJWTAuthenticationHandler
)

# Import the User model created in the last step
from user import User

# Create a Flask app
app = Flask(__name__)

# Create an authentication handler
authentication_handler = HTTPOAuth2BearerJWTAuthenticationHandler(
    # The secret used for generating JWT tokens
    key_or_secret='my-secret',
    # The algorithm used for generating JWT tokens
    algorithm='HS256',
    # Specify that the token comes in the URI query string of the HTTP request
    mode=HTTPOAuth2BearerJWTModes.URI_QUERY
)

# Create a nanopie microservice with the authentication handler just created
svc = FlaskService(app=app,
                   authn_handler=authentication_handler)

...
```

Run the script again:

``` sh
python main.py
```

Open the browser of your system and visit `127.0.0.1:8080/users/1`. Without
a valid token, your service should return a `401 Unauthorized` error.

You can generate a valid token using the algorithm and secret specified in
the code snippet. There are many Python packages available for this purpose;
you can also use [`jwt.io`](https://jwt.io/) to get a token for testing
purposes interactively. Alternatively, use the token below:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.EpM5XBzTJZ4J8AfoJEcJrjth8pfH28LWdjLo90sYb9g
```

And point your browser to `127.0.0.1/users/1?access_token=YOUR-ACCESS-TOKEN`
(replace `YOUR-ACCESS-TOKEN` with a token of your own). Your request is now
authenticated and you should see the user data returned to you.

### Adding logging and tracing capabilities

It is common for developers to use logging and tracing to observe their
microservices and API backends in action. Similar to authentication
handlers, nanopie provides a number of pluggable logging and tracing solutions
as well, integrating with the
[standard Python logging module](https://docs.python.org/3/library/logging.html)
and [OpenTelemetry](https://opentelemetry.io/) respectively.

To enable logging and tracing, edit `main.py` for another time and create
a `LoggingHandler` and `OpenTelemetryTracingHandler`:

``` python
from flask import Flask
from nanopie import (
    FlaskService,
    HTTPOAuth2BearerJWTModes,
    HTTPOAuth2BearerJWTAuthenticationHandler,
    LoggingHandler,
    OpenTelemetryTracingHandler
)

# Import the User model created in the last step
from user import User

# Create a Flask app
app = Flask(__name__)

# Create an authentication handler
...

# Create a logging handler and a tracing handler.
logging_handler = LoggingHandler()
tracing_handler = OpenTelemetryTracingHandler()

# Create a nanopie microservice with an authentication handler,
# a logging handler, and a tracing handler.
svc = FlaskService(app=app,
                   authn_handler=authentication_handler,
                   logging_handler=logging_handler,
                   tracing_handler=tracing_handler)
```


Run the script for another time:

``` sh
python main.py
```

Open the browser of your system and visit
`127.0.0.1/users/1?access_token=YOUR-ACCESS-TOKEN`. Check the output
in the terminal running the Python script, you should see outputs similar
to the snippets below:

```
# The log entry nanopie writes when the execution of an endpoint begins.
{"host": "YOUR-HOST", "logger": "nanopie.logging.base", "level": "INFO", "module": "base", "func": "__call__", "message": "Entering span unspecified_span."}

# The trace of the execution of the endpoint.
{"name": "unspecified", "context": {"trace_id": "7732924096377129845968717310647764965", "span_id": "7510401874971537686", "trace_state": "{}", "is_remote": "False"}, "kind": "SpanKind.SERVER", "parent": null, "start_time": "2020-08-11T20:23:01.350515Z", "end_time": "2020-08-11T20:23:01.351445Z", "attributes": "{}"}

# The long entry nanopie writes when the execution of an endpoint completes.
{"host": "YOUR-HOST", "logger": "nanopie.logging.base", "level": "INFO", "module": "base", "func": "__call__", "message": "Exiting span unspecified_span."}
```

## What's next

Learn more about nanopie in its [documentation](https://nanopie.readthedocs.io).
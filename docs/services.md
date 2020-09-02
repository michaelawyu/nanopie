# Services

A nanopie service consists of a number of endpoints, each equipped with
one or more handlers chained together for authentication,
serialization/deserialization, logging, tracing, and more.

Under the hood a nanopie service integrates with a Python web framework as
transport for the flow of data. Loosely speaking, you can think of nanopie
services as a way of helping you configure the web framework of your choice.
If you want to, you may still write your application logic following the
principles of your preferred frameworks.

nanopie plans to provide a variety of services of different types (HTTP,
event-driven, etc.) with support for different frameworks. At this early
stage of development, however, nanopie supports only HTTP (RESTful)
microservices/API backend with the Flask micro-framework as transport.

## Using HTTP services

You may use the following framework as transport with a nanopie HTTP service
at this moment:

Framework  | Service Class | Description
------------- | --------------------- | ----------------------
Flask | `FlaskService` | An HTTP service with the [Flask]((https://flask.palletsprojects.com/)) micro-framework as transport.

### Creating the service

To create a nanopie HTTP service, build an application using your
preferred framework and wrap it with the corresponding nanopie service class.

You must specify what data interchange format you would like to use for
serialization and deserialization when you create the service by setting up
a serialization helper. By default nanopie HTTP services use the JSON format;
if you would like to change this setting and use a different serialization
helper, see [Serialization](/serialization) for instructions. In addition, if
you have an authentication, logging, or tracing handler
that you would like to apply to all endpoints in a service, you should specify
them when you create the service as well.

=== "Flask"

    ```python
    from flask import Flask
    from nanopie import FlaskService

    app = Flask(__name__)
    svc = FlaskService(app=app)
    ```

??? "Service class arguments"

    Argument  | Required | Type and Default Value | Description
    ------------- | ------- | -------------- | ---------------------
    `app` | Yes | N/A | The application class from a transport.
    `authn_handler` | No | `AuthenticationHandler`, `None` | The authentication handler that the service should apply to all endpoints. See [Authentication](/authentication) for more information.
    `logging_handler` | No | `LoggingHandler`, `None` | The logging handler that the service should apply to all endpoints. See [Logging](/logging) for more information.
    `tracing_handler` | No | `TracingHandler`, `None` | The tracing handler that the service should apply to all endpoints. See [Tracing](/tracing) for more information.
    `serialization_helper` | No | `SerializationHelper`, `None` | The serialization helper that the service should use. See [Serialization](/serialization) for more information.
    `max_content_length` | No | `6000` | The maximum length of requests.

### Adding endpoints

A nanopie HTTP service provides a number of decorators for you to create
common HTTP RESTful endpoints:

Decorator  | RESTful Endpoint | Description
------------- | --------------------- | ----------------------
`create` | `CREATE` | A `CREATE` endpoint using the HTTP `POST` verb, usually used for create new resources.
`get` | `GET` | A `GET` (`READ`) endpoint using the HTTP `GET` verb, usually used for retrieving resources.
`update` | `UPDATE` | An `UPDATE` endpoint using the HTTP `PATCH` verb, usually used for updating resources.
`delete` | `DELETE` | A `DELETE` endpoint using the HTTP `DELETE` verb, usually used for deleting resources.
`list` | - | An endpoint using the HTTP `GET` verb, usually used for listing resources.
`custom` | - | An endpoint using a custom verb (mapped to one of the HTTP verbs), usually used for custom operations on resources.

```python
# svc is the nanopie service created in the previous step
# This will create an endpoint at `/users` that accepts HTTP GET requests
# and return a list of users.
@svc.list(name="list_users",
          rule="/users")
def list_users():
    do_something()

# This will create a custom endpoint at `/users/USER-ID:verify` with the `GET`
# HTTP verb for verifying users.
@svc.custom(name="verify_user",
            rule="/users/<int:user_id>",
            verb="GET",
            method="verify")
def verify_user(user_id):
    do_something()
```

If you prefer not using the decorators, nanopie services also provide the
following methods for creating endpoints; these methods take the same
arguments that decorators accept, with an addition, the `func` keyword argument.

* `add_create_endpoint`
* `add_get_endpoint`
* `add_update_endpoint`
* `add_delete_endpoint`
* `add_list_endpoint`
* `add_custom_endpoint`

``` python
def list_users():
    do_something()

svc.add_list_endpoint(name="list_users",
                      rule="/users",
                      func=list_users)
```

??? "Arguments for `create`, `get`, `update`, `delete`, and `list` decorators"

    Argument  | Required | Type and Default Value | Description
    ------------- | ------- | -------------- | ---------------------
    `name` | Yes | `str`, N/A | The name of the endpoint.
    `rule` | Yes | `str`, `None` | The URL rule associated with the endpoint. See [Rules](/services#rules) for more information.
    `data_cls` | Yes for `create` and `update` decorators | `ModelMetaCls`, N/A for `create` and `update` decorators, `None` for others | The data model for the request payload. See [Data models](/services#data-models) for more information.
    `headers_cls` | No | `ModelMetaCls`, `None` | The data model for the headers of requests. See [Data models](/services#data-models) for more information.
    `query_args_cls` | No | `ModelMetaCls`, `None` | The data model for the query arguments of requests. See [Data models](/services#data-models) for more information.
    `authn_handler` | No | `AuthenticationHandler`, `None` | The authentication handler applied to this endpoint. See [Endpoint specific authentication, logging, and tracing handlers](/services#endpoint-specific-authentication-logging-and-tracing-handlers) for more information.
    `logging_handler` | No | `LoggingHandler`, `None` | The logging handler applied to this endpoint. See [Endpoint specific authentication, logging, and tracing handlers](/services#endpoint-specific-authentication-logging-and-tracing-handlers) for more information.
    `tracing_handler` | No | `OpenTelemetryTracingHandler`, `None` | The tracing handler applied to this endpoint. See [Endpoint specific authentication, logging, and tracing handlers](/services#endpoint-specific-authentication-logging-and-tracing-handlers) for more information.
    `extras` | No | `Dict`, `None` | User-supplied additional information about the endpoint. See [Extras](/services#extras) for more information.

??? "Arguments for `custom` decorators"

    `custom` decorators support all the arguments of `create`, `get`, `update`,
    `delete`, and `list` decorations, with the following additional arguments:

    Additional Argument  | Required | Type and Default Value | Description
    ------------- | ------- | -------------- | ---------------------
    `verb` | Yes | `str`, N/A | The HTTP verb associated with the endpoint. It should be one of `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `UPDATE`, `TRACE`, `OPTIONS`, and `CONNECT`.
    `method` | Yes | `str`, N/A | The custom method, such as `verify`, associated with the endpoint.

#### Rules

Each endpoint is associated with a URL rule, which dictates the path of the
endpoint, such as `/users`. If the path includes a variable part (path
parameter), specify it with the syntax `<TYPE:NAME>`. For example, a
`GET` endpoint for a user management API may live at the path `/users/USER-ID`,
where the `USED-ID` is the integer ID of a user; and its URL rule should be
expressed as `/users/<int:user_id>`. nanopie will send the name of the variable
part and its value parsed from the URL to the decorated method as keyword
arguments.

The following types are available:

Type | Description
------------- | ---------------------
`string` | A string typed variable (without slashes).
`int` | An integer typed variable.
`float` | A float typed variable.
`path` | A string typed variable with slashes.
`any` | A variable of any type.
`uuid` | A UUID formatted string.

The code snippet below creates a `GET` endpoint for getting a user; if you
run the service and access `/users/1`, the `get_user` method will receive a
keyword argument `user_id=1`.

``` python
@svc.get(name="get_user",
         rule="/users/<int:user_id>")
def get_user(user_id):
    do_something()
```

#### Data models

Aside from the path parameters specified in the rules, HTTP microservices and API backends also accept parameters in the headers and query strings
of the HTTP request, with the resources themselves being transferred
in the payload. nanopie allows developers to model the parameters and
the resources with [nanopie data models](/data-model), and you can add
these models to your endpoints via the decorators so that nanopie services
can deserialize them from the raw data in the HTTP requests into instances
of your data models automatically.

The code snippet below creates a `CREATE` endpoint for creating a user; it
accepts HTTP requests with serialized `User` objects
(e,g, `{ "name": "Albert Wesker" }`, if using JSON as the data interchange
format) as payload. nanopie will deserialize the payload automatically into
an instance of the `User` data model; see [Requests](/requests) for
instructions on how to access it.

``` python
class User(Model):
    name = StringField()

@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    do_something()
```

#### Endpoint specific authentication, logging, and tracing handlers

You can add individual authentication, logging, and tracing handlers to an
endpoint. This will override the service-wide settings (if any).

!!! note

    See [Authentication](/authentication), [Logging](/logging), and
    [Tracing](/tracing) for
    instructions on using authentication, logging, and tracing handlers.

The code snippet below creates two endpoints, `get_user` and `create_user`,
with tracing enabled only on the `create_user` endpoint.

``` python
@svc.get(name="get_user",
         rule="/users/<int:user_id>")
def get_user(user_id):
    do_something()

tracing_handler = OpenTelemetryTracingHandler()

@svc.create(name="create_user",
            rule="/users",
            data_cls=User,
            tracing_handler=tracing_handler)
def create_user():
    do_something()
```

### Writing the application logic

As stated in the beginning of this document, in some way what nanopie does
is merely helping you configure your preferred framework for running
microservices and API backends. Therefore, when you use decorators
from nanopie services to decorate a method and write your application
logic for a specific endpoint in the method, most designs and patterns
from your preferred framework will continue to work. For example, if you are
using a Flask application as transport, you can still access the raw data in
the request using the `Flask.request` global proxy, or return an HTTP
response with the `make_response` method.

=== "Flask"

    ```python
    from flask import Flask, request, make_response
    from nanopie import FlaskService

    app = Flask(__name__)
    svc = FlaskService(app=app)

    @svc.get(name="get_user",
             rule="/users/<int:user_id>")
    def get_user(user_id):
        # Access the raw headers using the Flask request global proxy
        raw_headers = request.headers
        # Return a 500 response with the make_response method from Flask
        return make_response("Not implemented yet.", 500)
    ```

Still, nanopie offers its own ways to manipulate the flow of requests
and responses, as specified below. 

#### Requests

nanopie provides two global proxies, `request` and `parsed_request`, which
you can use to access information in incoming HTTP requests. As global
proxies, values in these proxies are set **when the service is running**;
an exception will be raised if you try to access them out of their contexts.

In nanopie HTTP services, `parsed_request` includes the headers, query
arguments, and the payload of incoming HTTP requests to a specific endpoint,
**deserialized as data model instances in accordance with the data models
specified when creating the endpoint**. The code snippet below showcases
how to access the data in requests payloads with the `parsed_request`
global proxy:

``` python
from nanopie import parsed_request

class User(Model):
    name = StringField()
    age = IntField()

@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    user = parsed_request.data
    print(user.name)
    print(user.age)
```

If the service uses JSON as data interchange format and you call the
`create_user` endpoint with `{ "name": "Albert Wesker", "age": 49 }`
as payload, you should see following output from the service:

```
Albert Wesker
49
```

Note that when deserializing data in HTTP requests based on a data model,
nanopie will ignore the hints and constraints specified in the data model.
Missing fields will be assigned the value `None`; fields that does not
exist in the data model but exists in the requests will be ignored. As such,
you should use the [built-in methods in data model](/data-model#using-models) instances to validate the data:

``` python
from nanopie import parsed_request

class User(Model):
    name = StringField(max_length=20, min_length=1)
    age = IntField(maximum=120, minimum=0)

@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    user = parsed_request.data
    try:
        user.validate()
    except ValidationError:
        return "Invalid input"
    
    print(user.name)
    print(user.age)
```

`parsed_request` proxies an `HTTPParsedRequest` object. Its attributes are:

Attributes | Type | Description
------------- | ---- | ---------------------
`headers` | `ModelMetaCls` | The headers in the incoming HTTP request parsed as data model instances.
`query_args` | `ModelMetaCls` | The query arguments in the incoming HTTP request parsed as data model instances.
`data` | `ModelMetaCls` | The payload in the incoming HTTP request parsed as data model instances.

On the other hand, `request` proxies an `HTTPRequest` object that includes
the raw data from the request. Its attributes are:

Attributes | Type | Description
------------- | ---- | ---------------------
`url` | `str` | The URL of the HTTP request.
`headers` | `Dict` | The headers of the HTTP request.
`content_length` | `int` | The content length of the HTTP request.
`mime_type` | `str` | The MIME type of the HTTP request.
`query_args` | `Dict` | The query arguments of the HTTP request.
`binary_data` | `bytes` | The binary payload of the HTTP request.
`text_data` | `bytes` | The text payload of the HTTP request.

``` python
from nanopie import equest

@svc.list(name="list_users",
          rule="/users")
def list_users():
    print(request.url)
    print(request.headers)
    print(request.query_args)
    print(request.text_data)
```

#### Responses

Most microservices and API backends return a resource (or a list of resources)
as responses. For example, a `CREATE` endpoint usually returns the created
resource and a `LIST` endpoint all listed resources. In nanopie HTTP services,
to accommodate this pattern, you can directly return nanopie data model
instances from decorated methods as response:

``` python
@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    return User(name="Albert Wesker", age=49)

@svc.list(name="list_users",
          rule="/users")
def list_users():
    return [
        User(name="Albert Wesker", age=49),
        User(name="Chris Redfield", age=47)
    ]
```

nanopie services will automatically serialize the returned data model
instances and build the HTTP response.

Alternatively, you can also use the `HTTPResponse` class to build
a response manually and return it:

``` python
from nanopie import HTTPResponse

@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    return HTTPResponse(status_code=200,
                        headers={},
                        mime_type="application/json",
                        data='{ "name": "Albert Wesker", "age": 49 }')
```

The `HTTPResponse` class has the following arguments:

Attributes | Type | Description
------------- | ---- | ---------------------
`status_code` | `int` | The status code of the HTTP response.
`headers` | `Dict` | The headers of the HTTP response.
`mime_type` | `str` | The MIME type of the payload in the HTTP response.
`data` | `str` or `bytes` | The payload of the HTTP response.

#### Other global proxies

Aside from the `request`, `parsed_request` global proxies, nanopie also provides
the following global proxies which you can use:

* `nanopie.svc` proxies the service itself
(`nanopie.services.http.HTTPService`),
allowing you to read the configuration of the service, such as the
default authentication, logging, and tracing handlers.

    ??? "Attributes of `HTTPService`"

        Attributes | Type | Description
        ------------- | ---- | ---------------------
        `endpoints` | `List[RPCEndpoint]` | A list of all endpoints.
        `authn_handler` | `AuthenticationHandler` | The default authentication handler for endpoints.
        `logging_handler` | `LoggingHandler` | The default logging handler for endpoints.
        `tracing_handler` | `OpenTelemetryTracingHandler` | The default tracing handler for endpoints.
        `serialization_helper` | `Serializationhelper` | The serializationn helper the service uses.
        `max_content_length` | `int` | The maximum length of requests.

* `nanopie.endpoint` proxies the endpoint
(`nanopie.services.RPCEndpoint`)
currently processing requests.

    ??? "Attributes of `RPCEndpoint`"

        Attributes | Type | Description
        ------------- | ---- | ---------------------
        `name` | `str` | The name of the endpoint.
        `rule` | `str` | The rule associated with the endpoint.
        `entrypoint` | `Handler` | The handler used as entrypoint.
        `extras` | `Dict` | Additional information about the endpoint.

### Running and Testing the service

Once again, as stated in the beginning of the document, using a nanopie
service should not stop you from running your application of your
preferred framework. You can still use the application object as you see
fit; if you plan to use an HTTP server such as
[`gunicorn`](https://gunicorn.org) for WSGI apps,
it will function normally as well.

=== "Flask"

    * Using the Flask developmental service

        ```python
        from flask import Flask
        from nanopie import FlaskService

        app = Flask(__name__)
        svc = FlaskService(app=app)

        @svc.get(name="get_user",
                rule="/users/<int:user_id>")
        def get_user(user_id):
            return "Hello World!"
        
        if __name__ == '__main__':
            # Run the app as configured by the nanopie Flask service
            # with the Flask developmental server
            app.run(debug=True, port=5000)
        ```
    
    * Using `gunicorn`

        ``` bash
        # The Python script above is avaiable at the path `main.py`
        gunicorn -w 4 main:app
        ```

# Exceptions

All nanopie exceptions are based on the `nanopie.misc.errors.ServiceError`
class. This class has four subclasses:

* `nanopie.misc.errors.AuthenticationError`: The class for all authentication
related exceptions.
* `nanopie.misc.errors.SerializationError`: The class for all serialization
related exceptions.
* `nanopie.misc.errors.ValidatorError`: The class for all data validation
related exceptions.
* `nanopie.misc.errors.FoundationError`: The class for exceptions in internal
handlers.

`ValidatorError` has its own subclasses, which you can catch when validating
data:

Exceptions | Field-related Error | Description
------------- | ------------- | -----------
`ModelTypeNotMatchedError` | No | The input data is not of the data model type used for validation.
`RequiredFieldMissingError` | Yes | A required field is missing (not assigned a value or assigned the value of `None`).
`FieldTypeNotMatchedError` | Yes | The input data is not of the data type specified in the field.
`ListItemTypeNotMatchedError` | Yes | One or more items in the input array (list) is not of the data type specified in the `ArrayField`.
`StringMaxLengthExceededError` | Yes | The input string is too long.
`StringMinLengthBelowError` | Yes | The input string is too short.
`StringPatternNotMatchedError` | Yes | The input string does not match the specified pattern.
`NumberMaxExceededError` | Yes | The input integer or float is too large.
`NumberMinBelowError` | Yes | The input integer or float is too small.
`ListTooManyItemsError` | Yes | The input array (list) has too many items.
`ListTooLitteItemsError` | Yes | The input array (list) has too little items.

These validation exceptions include additional information that details the
error; the following attributes are available:

* `source`: The field or data model used for data validation.
* `data`: The input data.
* `assigned_field_name`: The name of the field assigned in the data model.
This attribute is only available for field-related errors.
* `message`: The error message.

## Exceptions and responses

All nanopie exceptions have an attribute, `response`, defined in the
`ServiceError` base class, which accepts a `RPCResponse` object. When
an exception is raised in a nanopie service during the processing
of requests, the service checks if the `response` attribute is set. If so,
nanopie will return the specified response to the user (when applicable).
This is helpful when you would like to report user errors, such as invalid
input data, or unauthenticated requests, to users automatically.

The code snippet below specifies an endpoint in a nanopie HTTP service which
makes use of the `response` field in exceptions to return `400 Bad Request`
responses to users when the request data is invalid:

``` python
from flask import Flask
from nanopie import (
    FlaskService,
    Model,
    StringField,
    IntField,
    parsed_request,
    # HTTPResponse is a subclass of RPCResponse
    HTTPResponse
)
from nanopie.misc.errors import ValidationError

app = Flask(__name__)
svc = FlaskService(app=app)

class User(Model):
    name = StringField(max_length=20, min_length=1, required=True)
    age = IntField(maximum=120, minimum=0, required=True)

@svc.create(name="create_user",
            rule="/users",
            data_cls=User)
def create_user():
    user = parsed_request.data
    try:
        user.validate()
    except ValidationError as ex:
        # Set the response field and re-raise the exception
        # nanopie will return the HTTP response as specified
        ex.response = HTTPResponse(status_code=400,
                                   data="Bad request: Invalid user data.")
        raise ex
```
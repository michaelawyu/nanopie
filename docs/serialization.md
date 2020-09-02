# Serialization

As introduced in [Overview](/overview), nanopie provides pluggable solutions
for serialization and deserialization, in the form of serialization handlers.
A serialization handler works with a nanopie service to deserialize request
data from a specific data interchange format, such as JSON, to instances
of nanopie data models, and serialize instances of the same models (if any)
to response data in the same format.

Serialization handlers support different data interchange formats
using serialization helpers. nanopie provides a serialization handler for
each type of services it supports; you can mix and match serialization
helpers with the serialization handler of your service type to try out
different data interchange formats.

At this moment, nanopie provides the following serialization helpers and
serialization handlers:

Available Serialization Helper | Description
------------- | -------------
`JSONSerializationHelper` | The serialization helper for the JSON format.

Available Serialization Handler | Description
------------- | -------------
`HTTPSerializationHandler` | The serialization handler for HTTP services/API backend.

## Using serialization handlers

All nanopie services configure their serialization handlers automatically.
In most cases, you only need to specify the serialization helper (and
consequently the data interchange format) you would like to use.

The code snippet below configures a nanopie HTTP service with Flask as transport to use the JSON data interchange format for serialization/deserialization:

```python
from flask import Flask
from nanopie import (
    FlaskService,
    JSONSerializationHelper
)

app = Flask(__name__)
svc = FlaskService(app=app,
                   serialization_helper=JSONSerializationHelper())
```
# Logging

As introduced in [Overview](/overview), nanopie provides pluggable solutions
for logging, in the form of logging handlers. You may add logging handlers
to an endpoint or a service to log the beginning and the end of the processing
of a request automatically, or use these handlers separately in your code.

nanopie logging handers support structured logging and integrate closely with the
[standard Python logging module](https://docs.python.org/3/library/logging.html)
so as to provide an idiomatic logging solution. At its core, a logging handler
configures a Python logger with a formatter
([`logging.Formatter`](https://docs.python.org/3/library/logging.html#formatter-objects))
and a handler ([`logging.handler`](https://docs.python.org/3/library/logging.html#handler-objects)); the formatter accepts a dictionary (`Dict`) as
template and formats its key-value pairs using standard
[Python log record attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes), and the handler is responsible for transiting
the formatted logs, either in the form of a `Dict` or a JSON string, to
their destinations.

`LoggingHandler` is the foundation for all logging handlers in nanopie; this
handler simply writes logs (formatted as JSON strings) to standard streams.
Other logging handlers extend `LoggingHandler` and send logs to a variety
of destinations over the network, such as
[Fluentd](https://www.fluentd.org),
[Logstash](https://www.elastic.co/logstash), or
[Stackdriver Logging](https://cloud.google.com/logging).

## Using logging handlers

To add a logging handler to an endpoint or a service, specify it when
you create the endpoint or the service.

``` python
from flask import Flask
from nanopie import FlaskService, LoggingHandler

app = Flask(__name__)
svc = FlaskService(app=app)

logging_handler = LoggingHandler()

@svc.list(name="list_users",
          rule="/users/",
          logging_handler=logging_handler)
def list_users():
    do_something()
```

When added to an endpoint, the logging handler will log a message
(e.g. `Entering span list_users`) when a request arrives at the endpoint,
and another message (e.g. `Exiting span list_users`) when the endpoint
completes processing the request, along with other contextual information.
If you add a logging handler to a service, it will run for all the
endpoints in the service.

Alternatively, you may use a logging handler separately by getting the logger
it configures:

``` python
from nanopie import LoggingHandler

logging_handler = LoggingHandler()
logger = logging_handler.default_logger

logger.info("This is a test message.")
```

!!! note
    See [Python logging module](https://docs.python.org/3/library/logging.html#logrecord-attributes) for instructions on how to use Python loggers.

Logging handlers also include methods for setting up additional loggers.
To configure a non-root logger, call the `getLogger` method:

Arguments | Description
------------- | -------------
`name` | The name of the logger. See [`logging.getLogger`](https://docs.python.org/3/library/logging.html#logging.getLogger) for more information.
`append_handlers` | If set to `True`, the logging handler will set up a logger even if the logger already exists and has a handler specified. This may cause duplicate log entries when configured inappropriately. Defaults to `False`.

``` python
from nanopie import LoggingHandler

logging_handler = LoggingHandler()
logger = logging_handler.getLogger('example-logger')

logger.info("This is a test message.")
```

If you are feeling courageous, you may even use the `setup_root_logger` method
to set up the root logger with nanopie. This will process all log entries from a
Python program, including those who are emitted by loggers in other modules,
in the manner dictated by the nanopie logging handler. 

!!! note
    This may cause an infinite loop of failure if configured inappropriately
    since all Python loggers by default propagate to the root logger. See
    the `excluded_loggers` argument below for more information.

Arguments | Description
------------- | -------------
`excluded_loggers` | A list of loggers whose propagation will be disabled. This prevents error logs produced by erred handlers themselves being redirected back to these handlers. 
`append_handlers` | If set to `True`, the logging handler will set up the root logger even if it already has a handler specified. This may cause duplicate log entries when configured inappropriately. Defaults to `False`.

### Logs

Loggers configured by nanopie logging handlers by default logs messages
plus some contextual information in a structured manner using either the
`Dict` type or JSON strings.

For example, when running this code snippet

``` python
from nanopie import LoggingHandler

logging_handler = LoggingHandler()
logger = logging_handler.default_logger

logger.info("This is a test message.")
```

You should see the following output in the terminal (pretty-printed):

``` json
{
  "host": "HOSTNAME",
  "logger": "LOGGER",
  "level": "INFO",
  "module": "MODULE",
  "func": "FUNC",
  "message": "This is a test message."
}
```

The contextual information includes:

Attribute | Description
------------- | -------------
`host` | The hostname of the machine running the microservice/API backend. 
`logger` | The name of the logger that logs the message.
`level` | The level of the log message.
`module` | The module where the logger is called.
`func` | The function where the logger is called.

You can configure what additional context logging handlers should log along
with the message; it is even possible to ask these handlers to extract log
contexts from incoming requests automatically and send them along with
the log message. See the section below for instructions.

## Configuring logging handlers

Logging handlers provide the following options for configuring its logging
behavior:

Argument | Description
------------- | -------------
`default_logger_name` | The name of the logger that the logging handler itself uses. Defaults to `__name__`. If you plan to use different logging handlers in the same service/API backend, you should assign each of them a different `default_logger_name`. 
`span_name` | The name of the span. This value is used in the log messages that logging handlers output when being added to an endpoint or service. If not specified, logging handlers will try to use the name of the currently executing endpoint.
`level` | The level of the log message. See [Python Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels) for more information.
`fmt` | The format of the log message, in the form of a Dict. See the instructions below in this section for more information.
`datefmt` | The format of date and time (if any) in the log. See [Python Logging Date and Time Formatting](https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime) for more information.
`style` | How the values in the `fmt` Dict are formatted. It can be one of the three values: `%`, `{`, and `$`. See [Python Logging Formatting Styles](https://docs.python.org/3/library/logging.html#logging.Formatter) for more information.
`mode` | The mode this logging handler uses. See the instructions below in this section for more information.
`log_ctx_extractor` | A log context extractor that automatically extracts log contexts from requests. See the instructions below in this section for more information.
`quiet` |  If set to `True`, the logging handler runs quietly when extracting log contexts, i.e. it will not report any error should a log context cannot be extracted or processed.

### Formats

`fmt` is essentially a template of log entries that loggers configured
by nanopie logging handlers use to build structured logs. The default
`fmt` looks as follows:

``` python
{
    # hostname is the return of the socket.gethostname() method
    "host": "{}".format(hostname),
    "logger": "%(name)s",
    "level": "%(levelname)s",
    "module": "%(module)s",
    "func": "%(funcName)s",
}
```

Every time you call the configured logger to log a message, it will
replace the placeholders, such as `%(name)s` and `%(levelname)s`,
with available [Python Log Record Attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes), in the same way as the `str.format()` method
works.

You can update the `fmt` to include additional contextual information
in your logs. For example, with the `fmt` below configured loggers will
include the time when a message is logged in the structured logs:

``` python
from nanopie import LoggingHandler

logging_handler = LoggingHandler(fmt={"time": "%(asctime)s"})
logger = logging_handler.default_logger

logger.info("This is a test message.")
# The output should look like
# {"time": "2020-09-01 08:54:51,060", "message": "This is a test message."}
```

### Modes

`mode` controls how handlers in the configured loggers transmit log messages.
Three options are available:

* `SYNC`: Transmit logs synchronously.
* `BACKGROUND_THREAD`: Transmit logs asynchronously with a background thread.
* `ASYNC`: Transmit logs asynchronously in an event loop. This option only works when you are using configured loggers with an asynchronous framework,
such as `quart`, as transport.

The base `LoggingHandler` always work in the `SYNC` mode. This is
due to the fact that this logging handler only writes to the standard
streams on the local machine and it does not make sense to enable
asynchronous support.

!!! Note
    The available modes are listed in `nanopie.LoggingHandlerModes`. Instead
    of the raw values, you may also use `LoggingHandlerModes.SYNC`,
    `LoggingHandlerModes.BACKGROUND_THREAD`, or
    `LoggingHandlerModes.ASYNC`.

!!! Note
    At this early stage of development, some nanopie logging handlers have
    limited support for modes.

### Log context extractors

It is common for microservice and API backend developers to pass contextual
information in requests, so as to track user activities and/or system
workflow through services. A e-commerce service frontend, for example,
may pass the IDs of customers in requests; when processing the requests,
the backend will log the process with the IDs attached. The centralized
logging system can then correlate log entries using the IDs, granting
developers and operators a holistic view of interactions within a customer
session.

To support this use case, nanopie logging handler accepts a
`LogContextExtractor` as argument. When formatting a log message,
the formatter will invoke the log context extractor, which extracts
contextual information from the request currently being processed. You can
create a log context extractor by subclassing the `LogContextExtractor`
base class and override its `extract` method; the method should return
a nanopie data model (`Model`) as output, which will be merged into
the structured log:

``` python
from nanopie import Model, StringField, LogContextExtractor, LoggingHandler

# This is the data model for the log contexts in requests
class LogContext(Model):
    user_id = StringField()

class CustomLogContextExtractor(LogContextExtractor):
    # The `request` is the global request object
    # See the Services page of the documentation for more information
    def extract(self, request):
        user_id = request.headers.get('user_id')

        log_context = LogContext(user_id=user_id)
        return log_context

logging_handler = LoggingHandler(log_ctx_extractor=CustomLogContextExtractor())
```

## Connecting logging handlers to log collection services

The `LoggingHandler`, as specified in the beginning of this document, writes
all logs to the standard streams. If you would like to transmit logs
to other destinations, such as log collectors, nanopie provides a number
of additional logging handlers; they accept the same set of logging options and
function in the same way as the foundation `LoggingHandler`, with the only
difference being the destinations of logs.

Available Logging Handlers | Description
------------- | -------------
`FluentdLoggingHandler` | A logging handler that transmits logs to a Fluentd service. 
`LogstashLoggingHandler` | A logging handler that transmits logs to a Logstash service.
`StackdriverLoggingHandler` | A logging handler that transmits logs to Stackdriver Logging.

### Using `FluentdLoggingHandler`

Aside from the options inherited from `LoggingHandler`, this logging handler
accepts the following additional arguments:

Argument | Description
------------- | -------------
`host` | The hostname or address of the Fluentd service.
`port` | The port of the Fluentd service.
`tag` | The log entry tags.

``` python
from nanopie import FluentdLoggingHandler

logging_handler = FluentdLoggingHandler(host="HOST",
                                        port="PORT",
                                        tag="TAG")
logger = logging_handler.default_logger

logger.info("This is a test message")
```

### Using `LogstashLoggingHandler`

Aside from the options inherited from `LoggingHandler`, this logging handler
accepts the following additional arguments:

Argument | Description
------------- | -------------
`host` | The hostname or address of the Logstash service.
`port` | The port of the Logstash service.
`use_udp` | If set to `True`, the logs will be transmitted using the UDP protocol.

``` python
from nanopie import LogstashLoggingHandler

logging_handler = LogstashLoggingHandler(host="HOST",
                                         port="PORT",
                                         use_udp=False)
logger = logging_handler.default_logger

logger.info("This is a test message")
```

### Using `StackdriverLoggingHandler`

Aside from the options inherited from `LoggingHandler`, this logging handler
accepts the following additional arguments:

Argument | Description
------------- | -------------
`client` | A Stackdriver client.
`client_args` | Keyword arguments for the Stackdriver client. See [Stackdriver Client for Python](https://googleapis.dev/python/logging/latest/client.html) for more information.
`custom_log_name` | The name of the log entries in Stackdriver Logging. See [Stackdriver Logging Python Logging Handlers](https://googleapis.dev/python/logging/latest/handlers.html) for more information.
`resource` | The resource associated with the logs.
`labels` | The labels associated with the logs.
`stream` | The stream to use.

``` python
from google.cloud import logging
from nanopie import StackdriverLoggingHandler

stackdriver_client = logging.Client()
logging_handler = StackdriverLoggingHandler(client=stackdriver_client)
logger = logging_handler.default_logger

logger.info("This is a test message")
```

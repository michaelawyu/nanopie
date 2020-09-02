# Tracing

As introduced in [Overview], nanopie provides pluggable solutions
for tracing, in the form of tracing handlers. You may add tracing handlers
to an endpoint or a service to log the beginning and the end of the processing
of a request automatically, or use these handlers separately in your code.

nanopie tracing handlers integrate closely with [OpenTelemetry](https://opentelemetry.io/)
to provide a robust, portable, and industry standard tracing solution. At
its core, a tracing handler configures a OpenTelemetry tracer, which
traces an operation and exports the trace to its destination.

`OpenTelemetryTracingHandler` is the foundation for all tracing handlers
in nanopie; this handler simply writes the traces to the standard streams
in the form of JSON strings. Other tracing handlers extend
`OpenTelemetryTracingHandler` and add the capability of exporting traces
to a variety of destinations, including
[Jaeger](https://www.jaegertracing.io/) and [Zipkin](https://zipkin.io/).

## Using tracing handlers

To add a tracing handler to an endpoint or a service, specify it when you
create the endpoint or the service.

``` python
from flask import Flask
from nanopie import FlaskService, OpenTelemetryTracingHandler

app = Flask(__name__)
svc = FlaskService(app=app)

tracing_handler = OpenTelemetryTracingHandler()

@svc.list(name="list_users",
          rule="/users",
          tracing_handler=tracing_handler)
def list_users():
    do_something()
```

When added to an endpoint, the tracing handler will start a trace when
the endpoint starts processing a request, and ends the trace when
the endpoint finishes processing the request. If you add a tracing
handler to a service, it will run for all endpoints in the service.

Alternatively, you may use a tracing handler separately by getting the
OpenTelemetry tracer it configures:

``` python
from nanopie import OpenTelemetryTracingHandler

tracing_handler = OpenTelemetryTracingHandler()

tracer = tracing_handler.get_tracer())
```

!!! note
    See [OpenTelemetry for Python Documentation](https://opentelemetry-python.readthedocs.io/en/stable/index.html) for instructions on how to use the tracer.

## Configuring tracing handlers

Tracing handlers provide the following options for configuring its tracing
behavior:

Argument | Description
------------- | -------------
`with_span_name` | The name of the trace span. 
`with_span_attributes` | The attributes of the trace span.
`with_span_kind` | The kind of the trace span.
`with_endpoint_config` | If set to `True,` the tracing handler will add the basic information about the current endpoint to the span attributes.
`with_endpoint_extras` | If set to `True`, the tracing handler will add the user provided extra information about the current endpoint to the span attributes.
`propagated` | If set to `True`, trace propagation will be enabled. See the discussion below for more information.
`trace_ctx_extractor` | If set to `True`, the tracing handlers will run quietly when extracting trace contexts, i.e. it will not report any error should a trace context cannot be extracted or processed.
`batched` | If set to `True`, trace spans will be sent to sources in batch for better performance.
`with_sampler` | An OpenTelemetry trace sampler.
`probability` | The rate for probability sampling.
`write_to_console` | If set to `True`, the traces (spans) will be written to standard streams (stdout/stderr) in addition to source transmission.
`jsonprint` | If set to `True`, the traces (spans) will be output in the format of JSON strings when written to standard streams.

### Distributed tracing (trace context propagation)

It is common for a trace to span across a number of services; to correlate
spans, services must exchange (propagate) trace contexts, which is also
known as distributed tracing. nanopie tracing handlers support distributed
tracing via trace context extractors. Once configured with a trace context
extractor, tracing handlers will extract trace contexts automatically
when processing a request, and use the contexts to set up the trace (span).

To create a trace context extractor, subclass the `TraceContextExtractor`
class and override the `extract` method. It should return an instance
if the `TraceContext` class. For specifics, see the
[source code](https://github.com/michaelawyu/nanopie/blob/master/src/nanopie/tracing/base.py#L41).

For developers of HTTP microservices/API backends, W3C has [standardized
the way trace context is propagated in HTTP requests](https://www.w3.org/TR/trace-context/),
and nanopie provides a reference implementation of `TraceContext` and
`TraceContextExtractor` under the W3C standard that you can use:

``` python
from nanopie import (
    HTTPW3CTraceContext,
    HTTPW3CTraceContextExtractor,
    OpenTelemetryTracingHandler
)

trace_ctx_extractor = HTTPW3CTraceContextExtractor()
tracing_handler = OpenTelemetryTracingHandler(
    propagated=True,
    trace_ctx_extractor=http_w3c_trace_ctx_extractor
)
```

## Connecting tracing handlers to other services

The `OpenTelemetryTracingHandler`, as specified in the beginning of this
document, writes traces (trace spans) to the standard streams. If you
would like to send traces (trace spans) to other destinations, such
as distributed tracing systems, nanopie provides a number of additional
tracing handlers; they accept the same set of tracing options and function
in the same way as the foundation `OpenTelemetryTracingHandler`, with
the only difference being the destination of traces (trace spans).

Available Tracing Handlers | Description
------------- | -------------
`JaegerTracingHandler` | A tracing handler that transmits traces to a Jaeger service. 
`ZipkinTracingHandler` | A tracing handler that transmits traces to a Zipkin service.

### Using `JaegerTracingHandler`

Aside from the options inherited from `OpenTelemetryTracingHandler`, this
tracing handler accepts the following additional arguments:

Argument | Description
------------- | -------------
`service_name` | The name of the service.
`agent_host_name` | The hostname or address of the Jaeger agent.
`agent_port` | The port of the Jaeger agent.
`collector_host_name` | The hostname or address of the Jaeger collector.
`collector_port` | The port of the Jaeger collector.
`collector_endpoint` | The endpoint of the Jaeger collector.
`username` | The username.
`password` | The password.

``` python
from nanopie import JaegerTracingHandler

tracing_handler = JaegerTracingHandler(service_name="SERVICE")
```

### Using `ZipkinTracingHandler`

Aside from the options inherited from `OpenTelemetryTracingHandler`, this
tracing handler accepts the following additional arguments:

Argument | Description
------------- | -------------
`service_name` | The name of the service.
`host_name` | The hostname or address of the Zipkin service.
`port` | The port of the Zipkin service.
`endpoint` | The endpoint of the Zipkin service.
`protocol` | The protocol to use.
`ipv4` | Primary IPv4 address associated with this connection.
`ipv6` | Primary IPv6 address associated with this connection.
`retry` | If set to `True`, the exporter will retry upon failure.

``` python
from nanopie import ZipkinTracingHandler

tracing_handler = ZipkinTracingHandler(service_name="SERVICE")
```

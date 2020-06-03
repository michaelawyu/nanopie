import datetime
import json
import time

import pytest

from .marks import docker_installed, opentelemetry_installed, requests_installed
from nanopie.globals import svc_ctx, request
from nanopie.services.base import RPCEndpoint
from nanopie.tracing.base import OPENTELEMETRY_INSTALLED, OpenTelemetryTracingHandler
from nanopie.tracing.http_w3c_trace_ctx import (
    HTTPW3CTraceContext,
    HTTPW3CTraceContextExtractor,
)
from nanopie.tracing.jaeger import OPENTELEMETRY_JAEGER_INSTALLED, JaegerTracingHandler
from nanopie.tracing.zipkin import OPENTELEMETRY_ZIPKIN_INSTALLED, ZipkinTracingHandler


@pytest.fixture
def jaeger_container():
    try:
        import docker
    except ImportError:
        raise ImportError(
            "The docker (https://pypi.org/project/docker/)"
            "package is required to run this test. To "
            "install this package, run `pip install docker`."
        )

    docker_client = docker.from_env()
    jaeger_container = docker_client.containers.run(
        image="jaegertracing/all-in-one:1.17",
        ports={
            "5775/udp": 5775,
            "6831/udp": 6831,
            "6832/udp": 6832,
            5778: 5778,
            16686: 16686,
            14268: 14268,
            14250: 14250,
            9411: 9411,
        },
        detach=True,
        environment={"COLLECTOR_ZIPKIN_HTTP_PORT": 9411},
    )
    time.sleep(40)
    yield jaeger_container
    jaeger_container.kill()


@pytest.fixture
def zipkin_container():
    try:
        import docker
    except ImportError:
        raise ImportError(
            "The docker (https://pypi.org/project/docker/)"
            "package is required to run this test. To "
            "install this package, run `pip install docker`."
        )

    docker_client = docker.from_env()
    zipkin_container = docker_client.containers.run(
        image="openzipkin/zipkin", ports={9411: 9411}, detach=True
    )
    time.sleep(40)
    yield zipkin_container
    zipkin_container.kill()


@opentelemetry_installed
def test_opentelemetry_tracing_handler(capfd):
    tracing_handler = OpenTelemetryTracingHandler()

    assert tracing_handler() == None

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    assert span["context"]["trace_state"] == "{}"
    assert span["context"]["is_remote"] == "False"
    assert span["kind"] == "SpanKind.SERVER"
    assert span["parent"] == None
    assert span["start_time"] != None
    assert span["end_time"] != None
    assert span["attributes"] == "{}"


@opentelemetry_installed
def test_opentelemetry_tracing_handler_routes(capfd):
    tracing_handler = OpenTelemetryTracingHandler()

    def pseudo_handler(*args, **kwargs):
        time.sleep(1)
        return 0

    tracing_handler.add_route(name="test", handler=pseudo_handler)
    assert tracing_handler() == 0

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    assert span["context"]["trace_state"] == "{}"
    assert span["context"]["is_remote"] == "False"
    assert span["kind"] == "SpanKind.SERVER"
    assert span["parent"] == None
    assert span["start_time"] != None
    assert span["end_time"] != None
    assert span["attributes"] == "{}"

    start_time = span["start_time"][:-1]
    end_time = span["end_time"][:-1]
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f")

    elapsed = end_time - start_time
    assert elapsed.seconds >= 1


@pytest.mark.skipif(
    OPENTELEMETRY_INSTALLED,
    reason="requires that opentelemetry-api or opentelemetry-sdk is not installed",
)
def test_opentelemetry_tracing_handler_failure_opentelemetry_not_installed():
    with pytest.raises(ImportError) as ex:
        tracing_handler = (
            OpenTelemetryTracingHandler()
        )  # pylint: disable=unused-variable

    assert "opentelemetry-api" in str(ex.value)
    assert "opentelemetry-sdk" in str(ex.value)


@opentelemetry_installed
def test_opentelemetry_tracing_handler_user_extras(capfd):
    try:
        from opentelemetry import trace
    except ImportError:
        raise ImportError(
            "Packages opentelemetry-api "
            "(https://pypi.org/project/opentelemetry-api/) "
            "and opentelemtry-sdk "
            "(https://pypi.org/project/opentelemetry-sdk/) "
            "are required to run this test. To install "
            "these packages, run "
            "`pip install opentelemetry-api "
            "opentelemetry-sdk`"
        )

    tracing_handler = OpenTelemetryTracingHandler(
        with_span_name="span",
        with_span_attributes={"key": "value"},
        with_span_kind=trace.SpanKind.CONSUMER,
    )

    assert tracing_handler() == None

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "span"
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    assert span["context"]["trace_state"] == "{}"
    assert span["context"]["is_remote"] == "False"
    assert span["kind"] == "SpanKind.CONSUMER"
    assert span["parent"] == None
    assert span["start_time"] != None
    assert span["end_time"] != None

    span_attributes = json.loads(span["attributes"].replace("'", '"'))
    assert span_attributes["key"] == "value"


@opentelemetry_installed
def test_opentelemetry_tracing_handler_endpoint_extras(capfd, setup_ctx):
    tracing_handler = OpenTelemetryTracingHandler(
        with_span_name="span", with_endpoint_config=True, with_endpoint_extras=True
    )

    svc_ctx["endpoint"] = RPCEndpoint(
        name="endpoint", rule="rule", entrypoint=None, extras={"key": "value"}
    )

    assert tracing_handler() == None

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "span"
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    assert span["context"]["trace_state"] == "{}"
    assert span["context"]["is_remote"] == "False"
    assert span["kind"] == "SpanKind.SERVER"
    assert span["parent"] == None
    assert span["start_time"] != None
    assert span["end_time"] != None

    span_attributes = json.loads(span["attributes"].replace("'", '"'))
    assert span_attributes["endpoint.name"] == "endpoint"
    assert span_attributes["endpoint.rule"] == "rule"
    assert span_attributes["endpoint.extras.key"] == "value"


def test_http_w3c_trace_ctx_process():
    http_w3c_trace_ctx = HTTPW3CTraceContext(
        traceparent="00-a02996b5f223b9d785d9ac361fedb5b8-f4477120b9837b93-01",
        tracestate="rojo=00f067aa0ba902b7",
    )

    http_w3c_trace_ctx.process()
    assert http_w3c_trace_ctx.trace_id == 212892420273462992823733831323385443768
    assert http_w3c_trace_ctx.span_id == 17602162053966166931
    assert http_w3c_trace_ctx.trace_flags == 0
    assert http_w3c_trace_ctx.trace_state["rojo"] == "00f067aa0ba902b7"


def test_http_w3c_trace_ctx_extractor(capfd, setup_ctx):
    http_w3c_trace_ctx_extractor = HTTPW3CTraceContextExtractor()

    request.headers = {  # pylint: disable=assigning-non-slot
        "traceparent": "00-a02996b5f223b9d785d9ac361fedb5b8-f4477120b9837b93-01",
        "tracestate": "rojo=00f067aa0ba902b7",
    }

    http_w3c_trace_ctx = http_w3c_trace_ctx_extractor.extract(request=request)
    assert http_w3c_trace_ctx.trace_id == 212892420273462992823733831323385443768
    assert http_w3c_trace_ctx.span_id == 17602162053966166931
    assert http_w3c_trace_ctx.trace_flags == 0
    assert http_w3c_trace_ctx.trace_state["rojo"] == "00f067aa0ba902b7"


@opentelemetry_installed
def test_opentelemetry_tracing_handler_propagation(capfd):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider

    tracing_handler = OpenTelemetryTracingHandler(propagated=True)

    tracer_provider = TracerProvider()
    tracer = tracer_provider.get_tracer(__name__)

    parent_span_trace_id = ""
    with tracer.start_as_current_span("parent") as parent_span:
        tracing_handler()
        parent_span_trace_id = parent_span.context.trace_id

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"
    assert span["context"]["trace_id"] == str(parent_span_trace_id)


@opentelemetry_installed
def test_opentelemetry_tracing_handler_propagation_http_w3c(capfd, setup_ctx):
    http_w3c_trace_ctx_extractor = HTTPW3CTraceContextExtractor()
    tracing_handler = OpenTelemetryTracingHandler(
        propagated=True, trace_ctx_extractor=http_w3c_trace_ctx_extractor
    )

    request.headers = {  # pylint: disable=assigning-non-slot
        "traceparent": "00-a02996b5f223b9d785d9ac361fedb5b8-f4477120b9837b93-01",
        "tracestate": "rojo=00f067aa0ba902b7",
    }

    assert tracing_handler() == None

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"
    assert span["context"]["trace_id"] == "212892420273462992823733831323385443768"
    assert span["context"]["trace_state"] == "{'rojo': '00f067aa0ba902b7'}"


@opentelemetry_installed
def test_opentelemetry_tracing_handler_sampler(capfd):
    from opentelemetry.trace.sampling import ALWAYS_OFF

    tracing_handler = OpenTelemetryTracingHandler(with_sampler=ALWAYS_OFF)

    for i in range(10):  # pylint: disable=unused-variable
        tracing_handler()

    out, _ = capfd.readouterr()
    assert out == ""


@opentelemetry_installed
def test_opentelemetry_tracing_handler_probability(capfd):
    tracing_handler = OpenTelemetryTracingHandler(probability=0.0)

    for i in range(10):  # pylint: disable=unused-variable
        tracing_handler()

    out, _ = capfd.readouterr()
    assert out == ""


@opentelemetry_installed
def test_opentelemetry_tracing_handler_quiet(capfd):
    from nanopie.tracing.base import TraceContext, TraceContextExtractor

    class TC(TraceContext):
        @property
        def trace_id(self):
            raise RuntimeError

        @property
        def span_id(self):
            raise RuntimeError

        @property
        def trace_flags(self):
            raise RuntimeError

        @property
        def trace_state(self):
            raise RuntimeError

        def process(self):
            raise RuntimeError

    class TCE(TraceContextExtractor):
        def extract(self, request):
            return TC()

    tracing_handler = OpenTelemetryTracingHandler(trace_ctx_extractor=TCE(), quiet=True)

    tracing_handler()

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    int(span["context"]["trace_id"]).to_bytes(16, "little")
    assert span["context"]["trace_state"] == "{}"
    assert span["context"]["is_remote"] == "False"
    assert span["kind"] == "SpanKind.SERVER"
    assert span["parent"] == None
    assert span["start_time"] != None
    assert span["end_time"] != None
    assert span["attributes"] == "{}"


@opentelemetry_installed
def test_opentelemetry_tracing_handler_batched(capfd):
    tracing_handler = OpenTelemetryTracingHandler(batched=True)

    tracing_handler()

    out, _ = capfd.readouterr()
    assert out == ""

    time.sleep(6)

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["name"] == "unspecified"


@docker_installed
@requests_installed
def test_jaeger_tracing_handler(capfd, jaeger_container):
    assert jaeger_container.status in ["created", "running"]

    time.sleep(10)

    jaeger_tracing_handler = JaegerTracingHandler(service_name="service")
    jaeger_tracing_handler()

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["context"]["trace_id"]
    trace_id = hex(int(span["context"]["trace_id"]))[2:]

    time.sleep(10)

    import requests

    res = requests.get("http://localhost:16686/api/traces/{}".format(trace_id))
    assert res.status_code == 200


@pytest.mark.skipif(
    OPENTELEMETRY_JAEGER_INSTALLED,
    reason="requires that opentelemetry-ext-jaeger is not installed",
)
def test_jaeger_tracing_handler_failure_jaeger_ext_not_installed():
    with pytest.raises(ImportError) as ex:
        tracing_handler = JaegerTracingHandler(
            "service"
        )  # pylint: disable=unused-variable

    assert "opentelemetry-ext-jaeger" in str(ex.value)


@docker_installed
@requests_installed
def test_zipkin_tracing_handler(capfd, zipkin_container):
    assert zipkin_container.status in ["created", "running"]

    time.sleep(10)

    zipkin_tracing_handler = ZipkinTracingHandler(service_name="service")
    zipkin_tracing_handler()

    out, _ = capfd.readouterr()
    span = json.loads(out)
    assert span["context"]["trace_id"]
    trace_id = hex(int(span["context"]["trace_id"]))[2:]

    time.sleep(10)

    import requests

    res = requests.get("http://localhost:9411/api/v2/traces/{}".format(trace_id))
    assert res.status_code == 200


@pytest.mark.skipif(
    OPENTELEMETRY_ZIPKIN_INSTALLED,
    reason="requires that opentelemetry-ext-zipkin is not installed",
)
def test_zipkin_tracing_handler_failure_zipkin_ext_not_installed():
    with pytest.raises(ImportError) as ex:
        tracing_handler = ZipkinTracingHandler(
            "service"
        )  # pylint: disable=unused-variable

    assert "opentelemetry-ext-zipkin" in str(ex.value)

from typing import Optional

try:
    from opentelemetry.ext import jaeger

    OPENTELEMETRY_JAEGER_INSTALLED = True
except ImportError:
    OPENTELEMETRY_JAEGER_INSTALLED = False

from .base import OpenTelemetryTracingHandler


class JaegerTracingHandler(OpenTelemetryTracingHandler):
    """
    """

    def __init__(
        self,
        service_name: str,
        agent_host_name: str = "localhost",
        agent_port: int = 6831,
        collector_host_name: Optional[str] = None,
        collector_port: Optional[int] = None,
        collector_endpoint: str = "/api/traces?format=jaeger.thrift",
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs
    ):
        """
        """
        super().__init__(**kwargs)

        if not OPENTELEMETRY_JAEGER_INSTALLED:
            raise ImportError(
                "Packages opentelemetry-ext-jaeger "
                "(https://pypi.org/project/opentelemetry-ext-jaeger/) "
                "is required to enable Jaeger exporter. To "
                "install this package, run "
                "`pip install opentelemetry-ext-jaeger`"
            )

        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name=service_name,
            agent_host_name=agent_host_name,
            agent_port=agent_port,
            collector_host_name=collector_host_name,
            collector_port=collector_port,
            collector_endpoint=collector_endpoint,
            username=username,
            password=password,
        )
        self._span_processers.insert(0, self._processor(jaeger_exporter))

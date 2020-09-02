"""This module includes the tracing handler for connecting to the Zipkin service.
"""

from typing import Optional

try:
    from opentelemetry.ext import zipkin

    OPENTELEMETRY_ZIPKIN_INSTALLED = True
except ImportError:
    OPENTELEMETRY_ZIPKIN_INSTALLED = False

from .base import OpenTelemetryTracingHandler


class ZipkinTracingHandler(OpenTelemetryTracingHandler):
    """The tracing handler for connecting to Zipkin services."""

    def __init__(
        self,
        service_name: str,
        host_name: str = "localhost",
        port: int = 9411,
        endpoint: Optional[str] = "/api/v2/spans",
        protocol: Optional[str] = "http",
        ipv4: str = "",
        ipv6: str = "",
        retry: bool = False,
        **kwargs
    ):
        """Initializes a Zipkin tracing handler.

        Args:
            service_name (str): The name of the service.
            host_name (str): The hostname or address of the Zipkin service.
            port (int): The port of the Zipkin service.
            endpoint (str, Optional): The endpoint of the Zipkin service.
            protocol (str, Optional): The protocol to use.
            ipv4 (str): Primary IPv4 address associated with this connection.
            ipv6 (str): Primary IPv6 address associated with this connection.
            retry (bool): If set to True, the exporter will retry upon failure.
            **kwargs: Other keyword arguments for tracing handlers.
                See `OpenTelemetryTracingHandler`.
        """
        super().__init__(**kwargs)

        if not OPENTELEMETRY_ZIPKIN_INSTALLED:
            raise ImportError(
                "Packages opentelemetry-ext-zipkin "
                "(https://pypi.org/project/opentelemetry-ext-zipkin/) "
                "is required to enable Zipkin exporter. To "
                "install this package, run "
                "`pip install opentelemetry-ext-zipkin`"
            )

        zipkin_exporter = zipkin.ZipkinSpanExporter(
            service_name=service_name,
            host_name=host_name,
            port=port,
            endpoint=endpoint,
            protocol=protocol,
            ipv4=ipv4,
            ipv6=ipv6,
            retry=retry,
        )
        self._span_processers.insert(0, self._processor(zipkin_exporter))

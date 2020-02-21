from typing import Dict, Optional

try:
    from opentelemetry.ext import jaeger
    from opentelemetry.sdk.trace.export import (
        BatchExportSpanProcessor,
        ConsoleSpanExporter,
        SimpleExportSpanProcessor
    )
    OPENTELEMETRY_JAEGER_INSTALLED = True
except ImportError:
    OPENTELEMETRY_JAEGER_INSTALLED = False

from .base import OpenTelemetryTraceHandler

class JaegerTraceHandler(OpenTelemetryTraceHandler):
    """
    """
    def __init__(self,
                 service_name: str,
                 agent_host_name: str = 'localhost',
                 agent_port: int = 6831,
                 collector_host_name: Optional[str] = None,
                 collector_port: Optional[int] = None,
                 collector_endpoint: str = '/api/traces?format=jaeger.thrift',
                 username: Optional[str] = None,
                 password: Optionaxxl[str] = None,
                 with_span_name: Optional[str] = None,
                 with_span_attributes: Optional[Dict] = None,
                 with_span_kind: 'SpanKind' = trace.SpanKind.SERVER,
                 with_endpoint_config: bool = True,
                 with_endpoint_extras: bool = False,
                 propagated: bool = True,
                 with_sampler: Optional['Sampler'] = None,
                 probability: Optional[float] = None,
                 write_to_console: bool = True,
                 batched: bool = True):
        """
        """
        super().__init__(with_span_name=with_span_name,
                         with_span_attributes=with_span_attributes,
                         with_span_kind=with_span_kind,
                         with_endpoint_config=with_endpoint_config,
                         with_endpoint_extras=with_endpoint_extras,
                         propagated=propagated,
                         with_sampler=with_sampler,
                         probability=probability,
                         write_to_console=write_to_console)
        
        if not OPENTELEMETRY_JAEGER_INSTALLED:
            raise ImportError('Packages opentelemetry-ext-jaeger '
                              '(https://pypi.org/project/opentelemetry-ext-jaeger/) '
                              'is required to enable Jaeger exporter. To '
                              'install this package, run '
                              '`pip install opentelemetry-ext-jaeger`')
        
        jaeger_exporter = jaeger.JaegerSpanExporter(
            service_name=service_name,
            agent_host_name=agent_host_name,
            agent_port=agent_port,
            collector_host_name=collector_host_name,
            collector_port=collector_port,
            collector_endpoint=collector_endpoint,
            username=username,
            password=password
        )
        self._span_processers = []
        if batched:
            span_processor_jaeger = BatchExportSpanProcessor(jaeger_exporter)
            if write_to_console:
                span_processor_console = BatchExportSpanProcessor(
                    ConsoleSpanExporter()
                )
                self._span_processers = [
                    span_processor_jaeger,
                    span_processor_console
                ]
            else:
                self._span_processers = [ span_processor_jaeger ]
        else:
            span_processor_jaeger = SimpleExportSpanProcessor(jaeger_exporter)
            if write_to_console:
                span_processor_console = SimpleExportSpanProcessor(
                    ConsoleSpanExporter()
                )
                self._span_processers = [
                    span_processor_jaeger,
                    span_processor_console
                ]
            else:
                self._span_processers = [ span_processor_jaeger ]

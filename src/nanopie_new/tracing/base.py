from abc import abstractmethod
from typing import Dict

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import Tracer
    from opentelemetry.sdk.trace.export import (
        ConsoleSpanExporter,
        SimpleExportSpanProcessor
    )
    from opentelemetry.trace.sampling import ProbabilitySampler
    OPENTELEMETRY_INSTALLED = True
except ImportError:
    OPENTELEMETRY_INSTALLED = False

from ..globals import endpoint, tracing_ctx
from ..handler import Handler
from ..logger import logger
from ..misc import get_flattenable_dikt
from ..model import Model

class OpenTelemetryTraceHandler(Handler):
    """
    """
    def __init__(self,
                 with_span_name: Optional[str] = None,
                 with_span_attributes: Optional[Dict] = None,
                 with_span_kind: 'SpanKind' = trace.SpanKind.SERVER,
                 with_endpoint_config: bool = True,
                 with_endpoint_extras: bool = False,
                 propagated: bool = True,
                 with_sampler: Optional['Sampler'] = None,
                 probability: Optional[float] = None,
                 write_to_console: bool = True):
        """
        """
        if not OPENTELEMETRY_INSTALLED:
            raise ImportError('Packages opentelemetry-api '
                              '(https://pypi.org/project/opentelemetry-api/) '
                              'and opentelemtry-sdk '
                              '(https://pypi.org/project/opentelemetry-sdk/) '
                              'are required to enable tracing. To install '
                              'these packages, run '
                              '`pip install opentelemetry-api '
                              'opentelemetry-sdk`')

        self._with_span_name = with_span_name
        self._with_span_attributes = with_span_attributes
        self._with_span_kind = with_span_kind
        self._with_endpoint_config = with_endpoint_config
        self._with_endpoint_extras = with_endpoint_extras
        self._propagated = propagated
        if write_to_console:
            self._span_processers = [
                SimpleExportSpanProcessor(ConsoleSpanExporter())
            ]
        else:
            self._span_processers = []
        if with_sampler and probability:
            raise RuntimeError('Fields with_sampler and probability are '
                               'mutually exclusive.')
        elif not with_sampler and not probability:
            self._sampler = None
        else:
            self._sampler = with_sampler if with_sampler \
                else ProbabilitySampler(rate=probability)

        super().__init__()
    
    def __call__(self, *args, **kwargs):
        """
        """
        if self._propagated:
            try:
                trace.set_preferred_tracer_implementation(lambda T: Tracer())
            except RuntimeError:
                pass
            shared_tracer = trace.tracer()

            current_span = shared_tracer.get_current_span()
            if not current_span or \
               not current_span.get_context().is_valid():
                try:
                    trace_id = tracing_ctx.trace_id
                    span_id = tracing_ctx.span_id
                    trace_options = tracing_ctx.trace_options
                    trace_state = tracing_ctx.trace_state

                    current_span = trace.SpanContext(
                        trace_id=trace_id,
                        span_id=span_id,
                        trace_options=trace_options,
                        trace_state=trace_state)
                    assert(current_span.is_valid())
                except:
                    logger.warning('Trace context is not available; starting '
                                   'a new span without propagation instead.')
                    current_span = trace.INVALID_SPAN
            
            if self._sampler:
                tracer = Tracer(sampler=self._sampler)
            else:
                tracer = Tracer()
            
            for processor in self._span_processers:
                tracer.add_span_processor(processor)

            span_name = self._with_span_name
            if not span_name:
                span_name = endpoint.name
            
            span_attributes = {}
            span_attributes.update(
                get_flattenable_dikt(self._with_span_attributes))
            if self._with_endpoint_config:
                span_attributes.update(
                    get_flattenable_dikt({
                        'endpoint.name': endpoint.name,
                        'endpoint.rule': endpoint.rule
                    })
                )
            if self._with_endpoint_extras:
                span_attributes.update(
                    get_flattenable_dikt(endpoint.extras))
            
            span = tracer.start_span(span_name,
                                     parent=current_span,
                                     kind=self._with_span_kind,
                                     attributes=span_attributes)
            try:
                with tracer.use_span(span):
                    return super().__call__(*args, **kwargs)
            except:
                span.end()
                raise

class TraceContext(Model):
    """
    """
    @property
    @abstractmethod
    def trace_id(self) -> int:
        """
        """
        pass

    @property
    @abstractmethod
    def span_id(self) -> int:
        """
        """
        pass

    @property
    @abstractmethod
    def trace_options(self) -> 'TraceOptions':
        """
        """
        return trace.TraceOptions.get_default()

    @property
    @abstractmethod
    def trace_state(self) -> 'TraceState':
        """
        """
        return trace.TraceState.get_default()

    def process(self):
        """
        """
        pass

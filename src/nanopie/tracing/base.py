from abc import abstractmethod
from typing import Dict, Optional

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerSource
    from opentelemetry.sdk.trace.export import (
        BatchExportSpanProcessor,
        ConsoleSpanExporter,
        SimpleExportSpanProcessor,
    )
    from opentelemetry.trace.sampling import ProbabilitySampler

    OPENTELEMETRY_INSTALLED = True
except ImportError:
    OPENTELEMETRY_INSTALLED = False

from ..globals import endpoint, request as request_proxy
from ..handler import Handler
from ..logger import logger
from ..misc import get_flattenable_dikt
from ..model import Model
from ..services.base import Extractor


class TraceContext(Model):
    """
    """

    @property
    @abstractmethod
    def trace_id(self) -> int:
        """
        """

    @property
    @abstractmethod
    def span_id(self) -> int:
        """
        """

    @property
    @abstractmethod
    def trace_options(self) -> "TraceOptions":
        """
        """
        return trace.TraceOptions.get_default()

    @property
    @abstractmethod
    def trace_state(self) -> "TraceState":
        """
        """
        return trace.TraceState.get_default()

    def process(self):
        """
        """


class TraceContextExtractor(Extractor):
    """
    """

    @abstractmethod
    def extract(self, request: "RPCRequest") -> "TraceContext":
        """
        """


class OpenTelemetryTracingHandler(Handler):
    """
    """

    def __init__(
        self,
        with_span_name: Optional[str] = None,
        with_span_attributes: Optional[Dict] = None,
        with_span_kind: "SpanKind" = None,
        with_endpoint_config: bool = True,
        with_endpoint_extras: bool = False,
        propagated: bool = False,
        trace_ctx_extractor: Optional["TraceContextExtractor"] = None,
        quiet: bool = False,
        batched: bool = False,
        with_sampler: Optional["Sampler"] = None,
        probability: Optional[float] = None,
        write_to_console: bool = True,
    ):
        """
        """
        if not OPENTELEMETRY_INSTALLED:
            raise ImportError(
                "Packages opentelemetry-api "
                "(https://pypi.org/project/opentelemetry-api/) "
                "and opentelemtry-sdk "
                "(https://pypi.org/project/opentelemetry-sdk/) "
                "are required to enable tracing. To install "
                "these packages, run "
                "`pip install opentelemetry-api "
                "opentelemetry-sdk`"
            )

        self._with_span_name = with_span_name
        self._with_span_attributes = with_span_attributes
        self._with_span_kind = with_span_kind
        if not with_span_kind:
            self._with_span_kind = trace.SpanKind.SERVER
        self._with_endpoint_config = with_endpoint_config
        self._with_endpoint_extras = with_endpoint_extras

        self._propagated = propagated
        if propagated and not trace_ctx_extractor:
            raise ValueError(
                "trace_ctx_extractor is required " "for enabling propagation."
            )
        self._trace_ctx_extractor = trace_ctx_extractor
        self._quiet = quiet

        self._processor = (
            BatchExportSpanProcessor if batched else SimpleExportSpanProcessor
        )

        self._span_processers = []
        if write_to_console:
            self._span_processers.insert(0, self._processor(ConsoleSpanExporter))

        if with_sampler and probability:
            raise RuntimeError(
                "with_sampler and probability are " "mutually exclusive."
            )
        elif not with_sampler and not probability:
            self._sampler = trace.sampling.ALWAYS_ON
        else:
            self._sampler = (
                with_sampler if with_sampler else ProbabilitySampler(rate=probability)
            )

        self._tracer_source = None

        super().__init__()

    def _setup_tracer_source(self):
        """
        """
        if not self._tracer_source:
            tracer_source = TracerSource(sampler=self._sampler)
            for processor in self._span_processers:
                tracer_source.add_span_processor(processor)
            self._tracer_source = tracer_source

        return self._tracer_source

    def get_trace_ctx(self):
        """
        """
        if self._trace_ctx_extractor:
            return self._trace_ctx_extractor.extract(request=request_proxy)
        else:
            raise RuntimeError('trace_ctx_extractor is not present.')

    def get_tracer(self):
        """
        """
        tracer_source = self._setup_tracer_source()
        return tracer_source.get_tracer(__name__)

    def __call__(self, *args, **kwargs):
        """
        """
        tracer = self.get_tracer()
        current_span = tracer.get_current_span()
        if self._propagated:
            if not current_span or not current_span.get_context().is_valid():
                trace_ctx = self.get_trace_ctx()
                try:
                    trace_id = trace_ctx.trace_id
                    span_id = trace_ctx.span_id
                    trace_options = trace_ctx.trace_options
                    trace_state = trace_ctx.trace_state

                    current_span = trace.SpanContext(
                        trace_id=trace_id,
                        span_id=span_id,
                        trace_options=trace_options,
                        trace_state=trace_state,
                    )
                    assert current_span.is_valid()
                except Exception as ex:  # pylint: disable=broad-except
                    if not self._quiet:
                        raise ex

        span_name = self._with_span_name
        if not span_name:
            span_name = endpoint.name

        span_attributes = {}
        span_attributes.update(get_flattenable_dikt(self._with_span_attributes))
        if self._with_endpoint_config:
            span_attributes.update(
                get_flattenable_dikt(
                    {"endpoint.name": endpoint.name, "endpoint.rule": endpoint.rule}
                )
            )
        if self._with_endpoint_extras:
            span_attributes.update(get_flattenable_dikt(endpoint.extras))

        span = tracer.start_span(
            span_name,
            parent=current_span,
            kind=self._with_span_kind,
            attributes=span_attributes,
        )
        try:
            with tracer.use_span(span):
                return super().__call__(*args, **kwargs)
        except:
            span.end()
            raise

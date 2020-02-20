from abc import abstractmethod
from typing import Dict

try:
    from opentelemetry.trace.sampling import ProbabilitySampler
    OPENTELEMETRY_INSTALLED = True
except ImportError:
    OPENTELEMETRY_INSTALLED = False

from ..handler import Handler
from ..model import Model

class OpenTelemetryTraceHandler(Handler):
    """
    """
    def __init__(self,
                 with_span_name: Optional[str] = None,
                 with_span_attributes: Optional[Dict] = None,
                 with_endpoint_config: bool = True,
                 with_endpoint_extras: bool = False,
                 propagated: bool = True,
                 with_sampler: Optional['Sampler'] = None,
                 probability: Optional[float] = None):
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
        self._with_endpoint_config = with_endpoint_config
        self._with_endpoint_extras = with_endpoint_extras
        self._propagated = propagated
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
        raise NotImplementedError

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
    def trace_options(self) -> int:
        """
        """
        pass

    @property
    @abstractmethod
    def trace_state(self) -> Dict:
        """
        """
        pass

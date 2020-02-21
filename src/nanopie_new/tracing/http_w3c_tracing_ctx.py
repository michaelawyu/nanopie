import re

try:
    from opentelemetry import trace
except ImportError:
    pass

from .base import TraceContext
from ..fields import StringField

_KEY_WITHOUT_VENDOR_FORMAT = r'[a-z][_0-9a-z\-\*\/]{0,255}'
_KEY_WITH_VENDOR_FORMAT = (
    r'[a-z][_0-9a-z\-\*\/]{0,240}@[a-z][_0-9a-z\-\*\/]{0,13}'
)
_KEY_FORMAT = _KEY_WITHOUT_VENDOR_FORMAT + '|' + _KEY_WITH_VENDOR_FORMAT
_VALUE_FORMAT = (
    r'[\x20-\x2b\x2d-\x3c\x3e-\x7e]{0,255}[\x21-\x2b\x2d-\x3c\x3e-\x7e]'
)

_DELIMITER_FORMAT = '[ \t]*,[ \t]*'
_MEMBER_FORMAT = '({})(=)({})[ \t]*'.format(_KEY_FORMAT, _VALUE_FORMAT)
_DELIMITER_FORMAT_RE = re.compile(_DELIMITER_FORMAT)
_MEMBER_FORMAT_RE = re.compile(_MEMBER_FORMAT)

_TRACECONTEXT_MAXIMUM_TRACESTATE_KEYS = 32

_TRACEPARENT_HEADER_FORMAT = (
        "^[ \t]*([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})"
        + "(-.*)?[ \t]*$"
    )
_TRACEPARENT_HEADER_FORMAT_RE = re.compile(_TRACEPARENT_HEADER_FORMAT)

class HTTPW3CTraceContext(TraceContext):
    """
    """
    traceparent = StringField()
    tracestate = StringField()

    def process(self):
        """
        """
        if not self.traceparent:
            return

        match = re.search(_TRACEPARENT_HEADER_FORMAT_RE, self.traceparent)
        if not match:
            return
        
        version = match.group(1)
        trace_id = match.group(2)
        span_id = match.group(3)
        trace_options = match.group(4)

        if trace_id == "0" * 32 or span_id == "0" * 16:
            return

        if version == "00":
            if match.group(5):
                return
        if version == "ff":
            return

        self._extras['trace_id'] = int(trace_id, 16)
        self._extras['span_id'] = int(span_id, 16)
        self._extras['trace_options'] = trace.TraceOptions(trace_options)

        trace_state = trace.TraceState()
        count = 0

        for kv_pair in re.split(_DELIMITER_FORMAT_RE, self.tracestate):
            if not kv_pair:
                continue

            match = _MEMBER_FORMAT_RE.fullmatch(kv_pair)
            if not match:
                return
            
            k, _eq, v = match.groups()
            if k in trace_state:
                return
            
            trace_state[k] = v
            count += 1
            if count > _TRACECONTEXT_MAXIMUM_TRACESTATE_KEYS:
                return
        
        self._extras['trace_state'] = trace_state

    @property
    def trace_id(self) -> int:
        """
        """
        trace_id = self._extras.get('trace_id')
        if not trace_id:
            return 0

        return trace_id

    @property
    def span_id(self) -> int:
        """
        """
        span_id = self._extras.get('span_id')
        if not span_id:
            return 0
        
        return span_id

    @property
    def trace_options(self) -> 'TraceOptions':
        """
        """
        trace_options = self._extras.get('trace_options')
        if not trace_options:
            return trace.TraceOptions.get_default()
        
        return trace_options

    @property
    def trace_state(self) -> 'TraceState':
        """
        """
        trace_state = self._extras.get('trace_state')
        if not trace_state:
            return trace.TraceState.get_default()
        
        return trace_state

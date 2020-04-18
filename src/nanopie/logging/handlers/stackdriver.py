import datetime
from typing import BinaryIO, Dict, Optional, TextIO, Union

try:
    from google.cloud.logging.handlers.handlers import (
        CloudLoggingHandler,
        DEFAULT_LOGGER_NAME,
        _GLOBAL_RESOURCE,
    )
    from google.cloud.logging.handlers.transports.background_thread import (
        BackgroundThreadTransport,
        _DEFAULT_GRACE_PERIOD,
        _DEFAULT_MAX_BATCH_SIZE,
        _DEFAULT_MAX_LATENCY,
        _helpers,
        _Worker,
    )
    from google.cloud.logging.handlers.transports import SyncTransport
except ImportError:
    raise ImportError(
        "The google-cloud-logging "
        "(https://pypi.org/project/google-cloud-logging/)"
        "package is required to set up logging with Stackdriver. To "
        "install this package, run `pip install google-cloud-logging`."
    )


class PatchedSyncTransport(SyncTransport):
    """
    """

    def send(
        self,
        record: "LogRecord",
        message: Dict,
        resource: "google.cloud.logging.resource.Resource" = None,
        labels: Dict = None,
        trace: str = None,
        span_id: str = None,
    ):
        """
        """
        self.logger.log_struct(
            message,
            severity=_helpers._normalize_severity( # pylint: disable=protected-access
                record.levelno
            ),
            resource=resource,
            labels=labels,
            trace=trace,
            span_id=span_id,
        )


class PatchedWorker(_Worker):
    """
    """

    def enqueue(
        self,
        record: "LogRecord",
        message: Dict,
        resource: "google.cloud.logging.resource.Resource" = None,
        labels: Dict = None,
        trace: str = None,
        span_id: str = None,
    ):
        """
        """
        queue_entry = {
            "info": message,
            "severity": _helpers._normalize_severity( # pylint: disable=protected-access
                record.levelno
            ),
            "resource": resource,
            "labels": labels,
            "trace": trace,
            "span_id": span_id,
            "timestamp": datetime.datetime.utcfromtimestamp(record.created),
        }
        self._queue.put_nowait(queue_entry)


class PatchedBackgroundThreadTransport(BackgroundThreadTransport):
    """
    """

    def __init__( # pylint: disable=super-init-not-called
        self,  
        client: "google.cloud.logging.client.Client",
        name: str,
        grace_period: Union[int, float] = _DEFAULT_GRACE_PERIOD,
        batch_size: int = _DEFAULT_MAX_BATCH_SIZE,
        max_latency: Union[int, float] = _DEFAULT_MAX_LATENCY,
    ):
        """
        """
        self.client = client
        logger = self.client.logger(name)
        self.worker = PatchedWorker(
            logger,
            grace_period=grace_period,
            max_batch_size=batch_size,
            max_latency=max_latency,
        )
        self.worker.start()


class StackdriverHandler(CloudLoggingHandler):
    """
    """

    def __init__(
        self,
        client: "google.cloud.logging.client.Client",
        name: str = DEFAULT_LOGGER_NAME,
        transport: "google.cloud.logging.handlers.Transport" = PatchedBackgroundThreadTransport,
        resource: "google.cloud.logging.resource.Resource" = _GLOBAL_RESOURCE,
        labels: Optional[Dict] = None,
        stream: Optional[Union[TextIO, BinaryIO]] = None,
    ):
        """
        """
        super().__init__(
            client,
            name,
            transport,
            resource=resource,
            labels=labels,
            stream=stream,
        )

    def emit(self, record):
        """
        """
        message = self.formatter.format(record)
        self.transport.send(record, message, resource=self.resource, labels=self.labels)

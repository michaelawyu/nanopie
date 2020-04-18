import ast
import datetime
import logging
import time
import socket
from unittest.mock import MagicMock
import uuid

import pytest

from .marks import fluentd_installed, docker_installed, stackdriver_installed
from nanopie import StringField
from nanopie.globals import request
from nanopie.logger import logger as package_logger
from nanopie.logging import LogContext, LogContextExtractor, LoggingHandler, LoggingHandlerModes
from nanopie.logging.fluentd import FLUENT_INSTALLED, FluentdLoggingHandler
from nanopie.logging.logstash import LogstashLoggingHandler
from nanopie.logging.stackdriver import STACKDRIVER_INSTALLED, StackdriverLoggingHandler

DEFAULT_LOGGER_NAME = 'test'

@pytest.fixture
def simple_logging_handler():
    logging_handler = LoggingHandler()
    yield logging_handler
    logging_handler.default_logger.handlers = []

@pytest.fixture
def teardown_remove_logger_handlers():
    yield None
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    logger.handlers = []

@pytest.fixture
def fluentd_container():
    try:
        import docker
    except ImportError:
        raise ImportError(
            "The docker (https://pypi.org/project/docker/)"
            "package is required to run this test. To "
            "install this package, run `pip install docker`."
        )
    docker_client = docker.from_env()
    fluentd_container = docker_client.containers.run(
        image='nanopie-test/fluentd',
        ports={24224:24224},
        detach=True
    )
    time.sleep(10)
    yield fluentd_container
    fluentd_container.kill()

@pytest.fixture
def logstash_container():
    try:
        import docker
    except ImportError:
        raise ImportError(
            "The docker (https://pypi.org/project/docker/)"
            "package is required to run this test. To "
            "install this package, run `pip install docker`."
        )
    docker_client = docker.from_env()
    logstash_container = docker_client.containers.run(
        image='nanopie-test/logstash',
        ports={
            '9600/tcp':9600,
            '9600/udp':9600
        },
        detach=True,
        environment={'XPACK_MONITORING_ENABLED':'False'}
    )
    time.sleep(40)
    yield logstash_container
    logstash_container.kill()

@pytest.fixture
def stackdriver_logging_client():
    try:
        from google.cloud import logging
    except ImportError:
        raise ImportError(
            "The google-cloud-logging "
            "(https://pypi.org/project/google-cloud-logging/)"
            "package is required to run this test. To "
            "install this package, run `pip install google-cloud-logging`."
        )
    
    stackdriver_logging_client = logging.Client()
    return stackdriver_logging_client

def test_logging_handler(caplog, capsys, simple_logging_handler):
    with caplog.at_level(logging.INFO):
        res = simple_logging_handler()
    
    assert res == None
    assert caplog.record_tuples[0] == ('nanopie.logging.base', 20, 'Entering span unspecified_span.')
    assert caplog.record_tuples[1] == ('nanopie.logging.base', 20, 'Exiting span unspecified_span.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output_1 = ast.literal_eval(stderr_outputs[0])
    log_output_2 = ast.literal_eval(stderr_outputs[1])
    assert log_output_1['host'] == socket.gethostname()
    assert log_output_1['logger'] == 'nanopie.logging.base'
    assert log_output_1['level'] == 'INFO'
    assert log_output_1['module'] == 'base'
    assert log_output_1['func'] == '__call__'
    assert log_output_1['message'] == 'Entering span unspecified_span.'
    assert log_output_2['host'] == socket.gethostname()
    assert log_output_2['logger'] == 'nanopie.logging.base'
    assert log_output_2['level'] == 'INFO'
    assert log_output_2['module'] == 'base'
    assert log_output_2['func'] == '__call__'
    assert log_output_2['message'] == 'Exiting span unspecified_span.'

def test_logging_handler_dikt_message(caplog, capsys, simple_logging_handler):
    logger = simple_logging_handler.default_logger

    with caplog.at_level(logging.INFO):
        logger.info({'key': 'value'})
    
    assert caplog.record_tuples[0] == ('nanopie.logging.base', 20, "{'key': 'value'}")

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['host'] == socket.gethostname()
    assert log_output['logger'] == 'nanopie.logging.base'
    assert log_output['level'] == 'INFO'
    assert log_output['module'] == 'test_logging'
    assert log_output['func'] == 'test_logging_handler_dikt_message'
    assert log_output['key'] == 'value'

def test_logging_handler_get_logger(caplog, capsys, simple_logging_handler):
    logger = simple_logging_handler.getLogger('test_logger')

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert caplog.record_tuples[0] == ('test_logger', 20, 'This is a test message.')

def test_logging_handler_get_logger_failure_no_name(simple_logging_handler):
    with pytest.raises(ValueError) as ex:
        simple_logging_handler.getLogger('')
    
    assert 'use setup_root_logger method instead' in str(ex.value)

def test_logging_handler_setup_root_logger(caplog, capsys, simple_logging_handler):
    child_logger = logging.getLogger('child')
    child_logger.setLevel(logging.INFO)
    child_logger.addHandler(logging.StreamHandler())
    root_logger = simple_logging_handler.setup_root_logger(
        excluded_loggers=['child'],
        append_handlers=True)

    assert root_logger.name == 'root'
    assert root_logger.parent == None
    assert child_logger.propagate == False

    with caplog.at_level(logging.INFO):
        root_logger.info('This is a test message from root logger.')
        child_logger.info('This is a test message from child logger.')
    
    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == ('root', 20, 'This is a test message from root logger.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output_1 = ast.literal_eval(stderr_outputs[0])
    log_output_2 = stderr_outputs[1]
    assert log_output_1['host'] == socket.gethostname()
    assert log_output_1['logger'] == 'root'
    assert log_output_1['level'] == 'INFO'
    assert log_output_1['module'] == 'test_logging'
    assert log_output_1['func'] == 'test_logging_handler_setup_root_logger'
    assert log_output_1['message'] == 'This is a test message from root logger.'
    assert log_output_2 == 'This is a test message from child logger.'

def test_logging_handler_log_level(caplog, capsys, teardown_remove_logger_handlers):
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME, level=logging.WARNING)

    with caplog.at_level(logging.DEBUG):
        logging_handler()
    
    captured = capsys.readouterr()
    stdout_outputs = captured.out
    stderr_outputs = captured.err
    assert stdout_outputs == ''
    assert stderr_outputs == ''

def test_logging_handler_custom_fmt(caplog, capsys, teardown_remove_logger_handlers):
    fmt = {
        "logger": "%(name)s",
        "level": "%(levelname)s",
        "module": "%(module)s",
        "func": "%(funcName)s",
        "levelno": "%(levelno)s"
    }
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        fmt=fmt
    )
    logger = logging_handler.default_logger

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['logger'] == DEFAULT_LOGGER_NAME
    assert log_output['level'] == 'INFO'
    assert log_output['module'] == 'test_logging'
    assert log_output['func'] == 'test_logging_handler_custom_fmt'
    assert log_output['levelno'] == '20'

def test_logging_handler_custom_datefmt(caplog, capsys, teardown_remove_logger_handlers):
    fmt = {
        'logger': "%(name)s",
        'time': "%(asctime)s"
    }
    datefmt = "custom-datefmt-%Y-%m-%d %H:%M:%S,uuu"
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        fmt=fmt,
        datefmt=datefmt
    )
    logger = logging_handler.default_logger

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')
    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['logger'] == DEFAULT_LOGGER_NAME
    assert 'custom-datefmt' in log_output['time']

def test_logging_handler_custom_style_bracket(caplog, capsys, teardown_remove_logger_handlers):
    logging_handler = LoggingHandler(
        style='{',
        default_logger_name=DEFAULT_LOGGER_NAME
    )
    logger = logging_handler.default_logger

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')
    
    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['host'] == socket.gethostname()
    assert log_output['logger'] == 'test'
    assert log_output['level'] == 'INFO'
    assert log_output['module'] == 'test_logging'
    assert log_output['func'] == 'test_logging_handler_custom_style_bracket'

def test_logging_handler_custom_style_percent(caplog, capsys, teardown_remove_logger_handlers):
    logging_handler = LoggingHandler(
        style='$',
        default_logger_name=DEFAULT_LOGGER_NAME
    )
    logger = logging_handler.default_logger

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')
    
    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['host'] == socket.gethostname()
    assert log_output['logger'] == 'test'
    assert log_output['level'] == 'INFO'
    assert log_output['module'] == 'test_logging'
    assert log_output['func'] == 'test_logging_handler_custom_style_percent'

def test_logging_handler_quiet_mode(caplog, capsys, teardown_remove_logger_handlers):
    fmt = {
        'logger': "%(name)s",
        'missing_key': "%(missing_key)s"
    }
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        fmt=fmt,
        quiet=True
    )
    logger = logging_handler.default_logger

    logger.info('This is a test message.')

    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output['logger'] == 'test'
    assert log_output.get('missing_key') == None

def test_logging_handler_log_context_extractor(caplog, capsys, setup_ctx, teardown_remove_logger_handlers):
    class LoggingContext(LogContext):
        key = StringField()
    
    class LoggingContextExtractor(LogContextExtractor):
        def extract(self, request):
            value = request.headers.get('key')
            return LoggingContext(key=value)
    
    request.headers = {'key': 'value'} # pylint: disable=assigning-non-slot
    log_ctx_extractor = LoggingContextExtractor()

    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        log_ctx_extractor=log_ctx_extractor
    )
    logger = logging_handler.default_logger

    logger.info('This is a test message.')

    assert len(caplog.record_tuples) == 1
    assert caplog.record_tuples[0] == (DEFAULT_LOGGER_NAME, 20, 'This is a test message.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    log_output = ast.literal_eval(stderr_outputs[0])
    assert log_output.get('key') == 'value'

def test_logging_handler_failure_no_style(caplog, capsys, teardown_remove_logger_handlers):
    with pytest.raises(ValueError) as ex:
        logging_handler = LoggingHandler(
            default_logger_name=DEFAULT_LOGGER_NAME,
            style='^'
        )
        logger = logging_handler.default_logger # pylint: disable=unused-variable
    
    assert 'Style must be one of' in str(ex.value)

def test_logging_handler_failure_unfulfilled_key_in_fmt(caplog, capsys, teardown_remove_logger_handlers):
    fmt = {
        'logger': "%(name)s",
        'missing_key': "%(missing_key)s"
    }
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        fmt=fmt,
        quiet=False
    )
    logger = logging_handler.default_logger

    logger.info('This is a test message.')

    captured = capsys.readouterr()
    assert 'KeyError' in captured.err
    assert 'missing_key' in captured.err

def test_logging_handler_failure_log_context_extraction_error(caplog, capsys, setup_ctx, teardown_remove_logger_handlers):
    class LoggingContextExtractor(LogContextExtractor):
        def extract(self, request):
            raise RuntimeError

    log_ctx_extractor = LoggingContextExtractor()

    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        quiet=False,
        log_ctx_extractor=log_ctx_extractor
    )
    logger = logging_handler.default_logger
    logger.info('This is a test message.')

    captured = capsys.readouterr()
    assert 'Cannot extract log context' in captured.err
    assert 'RuntimeError' in captured.err

def test_logging_handler_get_log_ctx():
    class LoggingContext(LogContext):
        key = StringField()
    
    class LoggingContextExtractor(LogContextExtractor):
        def extract(self, request):
            value = request.headers.get('key')
            return LoggingContext(key=value)
    
    request.headers = {'key': 'value'} # pylint: disable=assigning-non-slot
    log_ctx_extractor = LoggingContextExtractor()
    logging_handler = LoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        log_ctx_extractor=log_ctx_extractor
    )
    log_ctx = logging_handler.get_log_ctx()

    assert log_ctx.key == 'value'

@docker_installed
@fluentd_installed
def test_fluentd_logging_handler(teardown_remove_logger_handlers, fluentd_container):
    assert fluentd_container.status in ['created', 'running']

    time.sleep(10)

    fluentd_logging_handler = FluentdLoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
    )
    logger = fluentd_logging_handler.default_logger
    logger.info('This is a test message.')

    time.sleep(20)

    logs = fluentd_container.logs().decode()

    assert 'app' in logs
    assert 'host' in logs
    assert socket.gethostname() in logs
    assert 'logger' in logs
    assert DEFAULT_LOGGER_NAME in logs
    assert 'level' in logs
    assert 'INFO' in logs
    assert 'module' in logs
    assert 'test_logging' in logs
    assert 'func' in logs
    assert 'test_fluentd_logging_handler' in logs
    assert 'message' in logs
    assert 'This is a test message' in logs

@pytest.mark.skipif(FLUENT_INSTALLED,
                    reason='requires that fluentd is not installed')
def test_fluentd_logging_handler_failure_fluentd_not_installed():
    with pytest.raises(ImportError) as ex:
        fluentd_logging_handler = FluentdLoggingHandler( # pylint: disable=unused-variable
            default_logger_name=DEFAULT_LOGGER_NAME
        )

    assert 'fluent-logger' in str(ex.value)

@docker_installed
def test_logstash_logging_handler_tcp(teardown_remove_logger_handlers, logstash_container):
    assert logstash_container.status in ['created', 'running']

    time.sleep(10)

    logstash_logging_handler = LogstashLoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME
    )
    logger = logstash_logging_handler.default_logger
    logger.info('This is a test message.')

    time.sleep(20)

    logs = logstash_container.logs().decode()

    assert 'app' in logs
    assert 'host' in logs
    assert socket.gethostname() in logs
    assert 'logger' in logs
    assert DEFAULT_LOGGER_NAME in logs
    assert 'level' in logs
    assert 'INFO' in logs
    assert 'module' in logs
    assert 'test_logging' in logs
    assert 'func' in logs
    assert 'test_fluentd_logging_handler' in logs
    assert 'message' in logs
    assert 'This is a test message' in logs

@docker_installed
def test_logstash_logging_handler_udp(teardown_remove_logger_handlers, logstash_container):
    assert logstash_container.status in ['created', 'running']

    time.sleep(10)

    logstash_logging_handler = LogstashLoggingHandler(
        default_logger_name=DEFAULT_LOGGER_NAME,
        use_udp=True
    )
    logger = logstash_logging_handler.default_logger
    logger.info('This is a test message.')

    time.sleep(20)

    logs = logstash_container.logs().decode()

    assert 'app' in logs
    assert 'host' in logs
    assert socket.gethostname() in logs
    assert 'logger' in logs
    assert DEFAULT_LOGGER_NAME in logs
    assert 'level' in logs
    assert 'INFO' in logs
    assert 'module' in logs
    assert 'test_logging' in logs
    assert 'func' in logs
    assert 'test_fluentd_logging_handler' in logs
    assert 'message' in logs
    assert 'This is a test message' in logs

@pytest.mark.skipif(STACKDRIVER_INSTALLED,
                    reason='requires that google-cloud-logging is not installed')
def test_stackdriver_logging_handler_failure_stackdriver_not_installed():
    with pytest.raises(ImportError) as ex:
        stackdriver_logging_handler = StackdriverLoggingHandler(
            client=None,
            default_logger_name=DEFAULT_LOGGER_NAME
        )

    assert 'google-cloud-logging' in str(ex.value)

@stackdriver_installed
def test_stackdriver_logging_handler_sync(teardown_remove_logger_handlers, stackdriver_logging_client):
    from google.cloud.logging.resource import Resource

    identifier = str(uuid.uuid4())
    resource = Resource(
        type="generic_node",
        labels={
            "location": "us-central1-a",
            "namespace": "default",
            "node_id": identifier,
        }
    )

    stackdriver_logging_handler = StackdriverLoggingHandler(
        client=stackdriver_logging_client,
        default_logger_name=DEFAULT_LOGGER_NAME,
        resource=resource
    )
    logger = stackdriver_logging_handler.default_logger
    logger.info('This is a test message.')

    time.sleep(20)

    _filter = 'resource.type = "generic_node" AND resource.labels.node_id = "{}"'.format(identifier)
    entries = []
    for entry in stackdriver_logging_client.list_entries(filter_=_filter):
        entries.append(entry)
    
    assert len(entries) == 1
    log = str(entries[0])
    assert 'host' in log
    assert socket.gethostname() in log
    assert 'logger' in log
    assert DEFAULT_LOGGER_NAME in log
    assert 'level' in log
    assert 'INFO' in log
    assert 'module' in log
    assert 'test_logging' in log
    assert 'func' in log
    assert 'test_fluentd_logging_handler' in log
    assert 'message' in log
    assert 'This is a test message' in log

@stackdriver_installedidentie
def test_stackdriver_logging_handler_background_thread():
    from google.cloud.logging.resource import Resource

    identifier = str(uuid.uuid4())
    resource = Resource(
        type="generic_node",
        labels={
            "location": "us-central1-a",
            "namespace": "default",
            "node_id": identifier,
        }
    )

    stackdriver_logging_handler = StackdriverLoggingHandler(
        client=stackdriver_logging_client,
        default_logger_name=DEFAULT_LOGGER_NAME,
        resource=resource,
        mode=LoggingHandlerModes.BACKGROUND_THREAD
    )
    logger = stackdriver_logging_handler.default_logger
    logger.info('This is a test message.')

    time.sleep(20)

    _filter = 'resource.type = "generic_node" AND resource.labels.node_id = "{}"'.format(identifier)
    entries = []
    for entry in stackdriver_logging_client.list_entries(filter_=_filter):
        entries.append(entry)
    
    assert len(entries) == 1
    log = str(entries[0])
    assert 'host' in log
    assert socket.gethostname() in log
    assert 'logger' in log
    assert DEFAULT_LOGGER_NAME in log
    assert 'level' in log
    assert 'INFO' in log
    assert 'module' in log
    assert 'test_logging' in log
    assert 'func' in log
    assert 'test_fluentd_logging_handler' in log
    assert 'message' in log
    assert 'This is a test message' in log

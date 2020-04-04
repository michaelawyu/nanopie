import ast
import logging
import socket

import pytest

from nanopie.logger import logger as package_logger
from nanopie.logging import LoggingHandler

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

def test_logging_handler_log_context_extractor(caplog, capsys):
    pass

def test_logging_handler_failure_no_style(caplog, capsys, teardown_remove_logger_handlers):
    with pytest.raises(ValueError) as ex:
        logging_handler = LoggingHandler(
            default_logger_name=DEFAULT_LOGGER_NAME,
            style='^'
        )
    
    assert 'Style must be one of' in str(ex.value)

def test_logging_handler_failure_unfulfilled_key_in_fmt(caplog, capsys, teardown_remove_logger_handlers):
    pass

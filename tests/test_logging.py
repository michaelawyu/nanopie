import ast
import logging
import socket

import pytest

from nanopie.logging import LoggingHandler

@pytest.fixture
def simple_logging_handler():
    return LoggingHandler()

def test_logging_handler(caplog, capsys, simple_logging_handler):
    with caplog.at_level(logging.INFO):
        simple_logging_handler()
    
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

def test_logging_handler_get_logger(caplog, capsys, simple_logging_handler):
    logger = simple_logging_handler.getLogger('test_logger')

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert caplog.record_tuples[0] == ('test_logger', 20, 'This is a test message.')

def test_logging_handler_get_logger_failure_no_name(simple_logging_handler):
    with pytest.raises(ValueError) as ex:
        logger = simple_logging_handler.getLogger('')
    
    assert 'use setup_root_logger method instead' in str(ex.value)

def test_logging_handler_setup_root_logger(caplog, capsys, simple_logging_handler):
    child_logger = logging.getLogger('child')
    child_logger.setLevel(logging.INFO)
    root_logger = simple_logging_handler.setup_root_logger(
        excluded_loggers=['child'])

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

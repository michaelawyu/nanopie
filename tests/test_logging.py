import ast
import logging
import socket

import pytest

from nanopie.logging import LoggingHandler

def test_logging_handler(caplog, capsys):
    logging_handler = LoggingHandler()

    with caplog.at_level(logging.INFO):
        logging_handler()
    
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

def test_logging_handler_get_logger(caplog, capsys):
    logging_handler = LoggingHandler()

    logger = logging_handler.getLogger('test_logger')

    with caplog.at_level(logging.INFO):
        logger.info('This is a test message.')
    
    assert caplog.record_tuples[0] == ('test_logger', 20, 'This is a test message.')

def test_logging_handler_setup_root_logger(caplog, capsys):
    pass

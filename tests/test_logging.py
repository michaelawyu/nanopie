import logging

from nanopie.logging import LoggingHandler

def test_logging_handler(caplog, capsys):
    logging_handler = LoggingHandler()

    with caplog.at_level(logging.INFO):
        logging_handler()
    
    assert caplog.record_tuples[0] == ('nanopie.logging.base', 20, 'Entering span unspecified_span.')
    assert caplog.record_tuples[1] == ('nanopie.logging.base', 20, 'Exiting span unspecified_span.')

    captured = capsys.readouterr()
    stderr_outputs = captured.err.split('\n')
    print(stderr_outputs)
    raise RuntimeError
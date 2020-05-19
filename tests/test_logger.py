from nanopie.logger import logger


def test_logger(caplog):
    message = "This is a test messge."
    logger.info(message)

    assert message in caplog.text

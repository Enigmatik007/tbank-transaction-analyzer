import logging
import pytest


@pytest.fixture(scope="session")
def logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("test_logger")

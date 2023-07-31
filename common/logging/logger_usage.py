from logger import Logger

logger = Logger(__name__).get_logger()


def some_function():
    try:
        # any code
        pass
    except Exception as e:
        logger.exception("An error occurred: %s", e)


logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

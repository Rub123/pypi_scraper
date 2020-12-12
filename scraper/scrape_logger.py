import logging

LOG_FILE = 'pypi_scraper.log'
LOGGER_NAME = 'pypi_logger'
FORMAT = logging.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
LEVEL = logging.INFO

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMAT)
FILE_HANDLER.setLevel(LEVEL)

PYPI_LOGGER = logging.getLogger(LOGGER_NAME)
PYPI_LOGGER.addHandler(FILE_HANDLER)

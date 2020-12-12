import logging
import sys

LOG_FILE = 'sqlalchemy.log'
LOGGER_NAME = 'sqlalchemy'
FORMAT = logging.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
LEVEL = logging.INFO

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMAT)
FILE_HANDLER.setLevel(LEVEL)

# STREAM_HANDLER = logging.StreamHandler(sys.stdout)
# STREAM_HANDLER.setLevel(LEVEL)
# STREAM_HANDLER.setFormatter(FORMAT)

SQL_LOGGER = logging.getLogger(LOGGER_NAME)
SQL_LOGGER.addHandler(FILE_HANDLER)
# SQL_LOGGER.addHandler(STREAM_HANDLER)

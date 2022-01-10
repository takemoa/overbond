import logging

from config import *


# setup file based logging at DEBUG level and console at INFO level
def setup_logging():
    # TODO RotatingFileHandler
    # File logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s %(asctime)s %(levelname)s %(message)s',
                        filename=LOG_FILE, filemode='a')

    # Console logger
    # define a new Handler to log to console as well
    console = logging.StreamHandler()
    # optional, set the logging level
    console.setLevel(logging.INFO)
    # set a format which is the same for console use
    # formatter = logging.Formatter('%(asctime)s %(message)s')
    formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)

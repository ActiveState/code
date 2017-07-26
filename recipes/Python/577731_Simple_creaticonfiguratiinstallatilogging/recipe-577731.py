from logging import Formatter, FileHandler, StreamHandler, getLogger
class LowPassFilter(logging.Filter):
    """Only allow messages at or below the threshold."""
    def __init__(self, threshold):
        super(LowPassFilter, self).__init__()
        self.threshold = threshold

    def filter(self, record):
        return record.levelno <= self.threshold

def addHandler(handler=None, stream=None, filename=None, filemode='a',
               format=None, datefmt=None, level=None, max_level=None,
               filters=(), logger=None):
    """stream, filename, filemode, format, datefmt: as per logging.basicConfig

       handler: use a precreated handler instead of creating a new one
       logging: logging to add the handler to (uses root logging if none specified)
       filters: an iterable of filters to add to the handler
       level: only messages of this level and above will be processed
       max_level: only messages of this level and below will be processed
    """
    # Create the handler if one hasn't been passed in
    if handler is None:
        if filename is not None:
            handler = FileHandler(filename, filemode)
        else:
            handler = StreamHandler(stream)
    # Set up the formatting of the log messages
    # New API, so it can default to str.format instead of %-formatting
    formatter = Formatter(format, datefmt)
    handler.setFormatter(formatter)
    # Set up filtering of which messages to handle
    if level is not None:
        handler.setLevel(level)
    if max_level is not None:
        handler.addFilter(LowPassFilter(max_level))
    for filter in filters:
        handler.addFilter(filter)
    # Add the fully configured handler to the specified logging
    if logger is None:
        logger = getLogger()
    logger.addHandler(handler)
    return handler

import logging, sys
# Let root logging handlers see all messages
logging.getLogger().setLevel(logging.NOTSET)
# Send WARNING and above to stderr
addHandler(stream=sys.stderr, level=logging.WARNING)
# Send DEBUG and INFO to stdout
addHandler(stream=sys.stdout, level=logging.INFO, max_level=logging.INFO)

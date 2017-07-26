from logging import Formatter, FileHandler, StreamHandler, getLogger
def addHandler(*, handler=None, stream=None, filename=None, filemode='a',
                  format=None, datefmt=None, style='{',
                  level=None, max_level=None, filters=(),
                  logger=None):
    """stream, filename, filemode, format, datefmt: as per logging.basicConfig

       handler: use a precreated handler instead of creating a new one
       logger: logger to add the handler to (uses root logger if none specified)
       filters: an iterable of filters to add to the handler
       level: only messages of this level and above will be processed
       max_level: only messages of this level and below will be processed
       style: as per logging.basicConfig, but defaults to '{' (i.e. str.format)
    """
    # Create the handler if one hasn't been passed in
    if handler is None:
        if filename is not None:
            handler = FileHandler(filename, filemode)
        else:
            handler = StreamHandler(stream)
    # Set up the formatting of the log messages
    # New API, so it can default to str.format instead of %-formatting
    formatter = Formatter(format, datefmt, style)
    handler.setFormatter(formatter)
    # Set up filtering of which messages to handle
    if level is not None:
        handler.setLevel(level)
    if max_level is not None:
        def level_ok(record):
            return record.levelno <= max_level
        handler.addFilter(level_ok)
    for filter in filters:
        handler.addFilter(filter)
    # Add the fully configured handler to the specified logger
    if logger is None:
        logger = getLogger()
    logger.addHandler(handler)
    return handler

# Example of setting up the logging module to direct raw output to
# sys.stdout and sys.stderr as appropriate
import sys, logging
# Let root logger handlers see all messages
logging.getLogger().setLevel(logging.NOTSET)
# Send WARNING and above to stderr
addHandler(stream=sys.stderr, level=logging.WARNING)
# Send INFO to stdout
addHandler(stream=sys.stdout, level=logging.INFO, max_level=logging.INFO)

logging.info("Hello world!") # only displayed once
logging.warn("Hello world!") # only displayed once

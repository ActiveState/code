for _name, logger in logging.Logger.manager.loggerDict:
    try:
        logger.setLevel(logging.ERROR)
    # skip "PlaceHolder" loggers
    except AttributeError:
        pass

## easy logging with extrasOriginally published: 2010-11-02 10:04:14 
Last updated: 2010-11-02 10:04:15 
Author: Bud P. Bruegger 
 
The logging package offers the "extra" keyword argument in Logger.log to add user-defined attributes to the log record.  LoggerAdaptors make it easy to use extras that are constant for a given logger;  then simply use logger.debug, logger.info, ecc.  But this won't support variable extra arguments.  \n\nThe present recipe makes it easy to use "extra" attributes that are not constant but variables passed to the (modified) logging methods ('debug', 'info', ...)
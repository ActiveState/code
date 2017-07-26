#!/usr/bin/env python

import logging

def processArgs(self, *args):
    msg = args[-1]
    args = args[:-1]
    # the following allows logging even in case of problems!
    if not (len(args) == len(self.extras)):
        noArgs = len(self.extras)
        l = list(' ' * noArgs)
        l[:len(args)] = args[:len(l)]
        print "WARNING: wrong number of logging arguments"
        args = l
    extras = dict(zip(self.extras, args))
    return (msg, extras)

def myLog(self, level, *args):
    if self.isEnabledFor(level):
        msg, extras = self.processArgs(*args)
        self._log(level, msg, [], extra=extras)

def myDebug(self, *args):
    self.log(logging.DEBUG, *args)

def myInfo(self, *args):
    self.log(logging.INFO, *args)

def myWarning(self, *args):
    self.log(logging.WARNING, *args)

def myError(self, *args):
    self.log(logging.ERROR, *args)

def myCritical(self, *args):
    self.log(logging.CRITICAL, *args)

def setLoggerExtras(logger, extras):
    logger.extras = extras
    logger.__class__.processArgs = processArgs
    logger.__class__.log = myLog
    logger.__class__.debug = myDebug
    logger.__class__.info = myInfo
    logger.__class__.warning = myWarning
    logger.__class__.error = myError
    logger.__class__.critical = myCritical

#-------------------------------------------------
if __name__ == '__main__':

    import logging.handlers

    def getRotFileLogger(name, filePath, maxBytes, maxCount, 
        logLevel=logging.DEBUG, format=None):
        format = format or '%(asctime)s - %(levelname)s - %(message)s'
        my_logger = logging.getLogger(name)
        my_logger.setLevel(logLevel)
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      filePath, maxBytes=maxBytes, backupCount=maxCount)
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
        return my_logger

    format = '%(asctime)s - %(levelname)s - %(extra1)s - %(extra2)s - %(message)s'
    logger = getRotFileLogger('test', 'test.log', 1000, 10, format=format)
    
    # simply set the extras
    setLoggerExtras(logger, ['extra1', 'extra2'])

    # and then log without explicit "extra" dict
    logger.debug('xx1', 'xx2', 'debug')
    logger.info('xx1', 'info')  #missing arg
    logger.warning('xx1', 'xx2', 'xx3', 'hello, a warning') #too many args
    logger.error('some error')
    logger.critical('some critical')
    

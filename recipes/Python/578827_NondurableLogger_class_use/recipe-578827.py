#!/usr/bin/python3
import sys
import os
import logging
import traceback
import time
import random
import inspect
import concurrent.futures
import warnings 

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

FMT_PID = '{asctime} {name} {process} {levelname} {message}'
logging.basicConfig(format=FMT_PID, style='{', level=logging.DEBUG)
#logging.basicConfig(filename='example.log', format=FMT_PID, style='{', level=logging.DEBUG)
LOGGER_NAME = 'mylogger'
_log = logging.getLogger(LOGGER_NAME)


class LM(object):  # allows str.format log messages to be used
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.msg.format(*self.args, **self.kwargs)


class NondurableLogger(object):
    """ This class supports a subset of logging.Logger features for use with concurrent.futures.ProcessPoolExecutor.
   
    Usage:
    
    The functions executed by the ProcessPoolExecutor's submit and map methods should create an instance of this
    class, use its methods to log messages, and return it along with their result.  The supervising process is
    responsible for handling the worker process log records - normally this is done by passing an appropriate
    Logger to the NondurableLogger.handle method.

    Although the stored log records are perishable, reasonable durability can be obtained by judicious use of
    exception handling in the functions executed by the ProcessPoolExecutor submit and map methods.
    
    Notes:

        1) threading.Lock cannot be pickled
        2) this class makes no promise of thread safety

    """

    def __init__(self, name, *, capacity=1000):
        if not isinstance(capacity, int):
            raise TypeError('capacity must be an integer')

        if capacity <= 0:
            raise ValueError('capacity must be a positive integer')

        self.name = name
        self._capacity = capacity
        self._records = []
        self._make_record = logging.getLogRecordFactory()

    def log_(self, lvl, msg, *args, **kwargs):
        if not isinstance(lvl, int):
            raise TypeError('level must be an integer')

        if len(self._records) >= self._capacity:
            warnings.warn('{0} capacity is full {1}'.format(type(self).__qualname__, os.getpid()))
        else:
            if not isinstance(msg, str):
                msg = str(msg)

            caller = inspect.currentframe().f_back.f_back
            fname, lineno, *_ = inspect.getframeinfo(caller)
            exc_info = sys.exc_info() if 'exc_info' in kwargs and kwargs['exc_info'] else None

            if not exc_info is None:
                tb = ''.join(traceback.format_exception(*exc_info))
                msg = '\n'.join((msg, tb))

            rec = self._make_record(self.name, lvl, fname, lineno, msg, args, None)
            self._records.append(rec)

    def debug(self, msg, *args):
        self.log_(logging.DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log_(logging.INFO, msg, *args)

    def warning(self, msg, *args):
        self.log_(logging.WARNING, msg, *args)

    def error(self, msg, *args):
        self.log_(logging.ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log_(logging.CRITICAL, msg, *args)

    def exception(self, msg, *args):
        self.log_(logging.ERROR, msg, *args, exc_info=True)

    def handle(self, target):
        assert isinstance(target, logging.Logger)

        for rec in self._records:
            target.handle(rec)

    def records(self):
        return self._records


def do_work(url, doze):
    result = None
    ndl = NondurableLogger(LOGGER_NAME)

    try:
        ndl.info(LM('converting {0}', url))
        result = url.replace('http', 'https')
        ndl.debug(LM('sleeping for {0}', doze))
        time.sleep(doze)

        if doze > 3:
            ndl.warning('very slow')

        num = len(result)/doze
        ndl.debug(LM('quotient {0}', num))
    except Exception:
        ndl.exception(LM('division by {0}', doze))

    return result, ndl


def main():
    _log.info('start')
    workers = 5

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        cf_doze = [random.randint(0, 5) for _ in URLS]
        args = (URLS, cf_doze)

        for url, ndl in executor.map(do_work, *args):
            ndl.handle(_log)
            _log.info(LM('>> {0}', url))

    _log.info('end')

if __name__ == '__main__':
    main()

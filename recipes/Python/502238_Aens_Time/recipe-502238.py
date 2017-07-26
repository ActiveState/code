'''Module for Aens time conversions.

This module provides several functions that allow
conversion from earth seconds to Aens time units.'''

__version__ = '1.0'

import sys as _sys
import thread as _thread
import time as _time

################################################################################

EPOCH_CORRECTION = 946684800
MILLE_PER_DAY = 1000000
KHILIOI_PER_DAY = 1000
DAYS_PER_WEEK = 7
WEEKS_PER_MONTH = 4
MONTHS_PER_SEASON = 3
SEASONS_PER_YEAR = 4
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = SECONDS_PER_DAY * DAYS_PER_WEEK
SECONDS_PER_MONTH = SECONDS_PER_WEEK * WEEKS_PER_MONTH
SECONDS_PER_SEASON = SECONDS_PER_MONTH * MONTHS_PER_SEASON
SECONDS_PER_YEAR = SECONDS_PER_SEASON * SEASONS_PER_YEAR

################################################################################

def seconds():
    'Return seconds since the epoch.'
    return _time.time() - EPOCH_CORRECTION

def mille(seconds):
    'Convert from seconds to mille.'
    return int(seconds % SECONDS_PER_DAY * MILLE_PER_DAY / SECONDS_PER_DAY % KHILIOI_PER_DAY)

def khilioi(seconds):
    'Convert from seconds to khilioi.'
    return int(seconds % SECONDS_PER_DAY * KHILIOI_PER_DAY / SECONDS_PER_DAY)

def day(seconds):
    'Convert from seconds to day.'
    return int(seconds) / SECONDS_PER_DAY % DAYS_PER_WEEK + 1

def week(seconds):
    'Convert from seconds to week.'
    return int(seconds) / SECONDS_PER_WEEK % WEEKS_PER_MONTH + 1

def month(seconds):
    'Convert from seconds to month.'
    return int(seconds) / SECONDS_PER_MONTH % MONTHS_PER_SEASON + 1

def season(seconds):
    'Convert from seconds to season.'
    return int(seconds) / SECONDS_PER_SEASON % SEASONS_PER_YEAR + 1

def year(seconds):
    'Convert from seconds to year.'
    return int(seconds) / SECONDS_PER_YEAR + 1

################################################################################

UNITS = year, season, month, week, day, khilioi, mille

def format(seconds, format='%u.%u.%u.%u.%u.%03u.%03u', units=UNITS):
    'Convert from seconds to string.'
    return format % tuple(function(seconds) for function in units)

################################################################################

class Mille_Timer:

    'Mille_Timer(function, *args, **kwargs) -> Mille Timer'

    def __init__(self, function, *args, **kwargs):
        'Initialize the Mille_Timer object.'
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__status = False
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Mille_Timer object.'
        self.__lock.acquire()
        self.__status = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__run, ())
        self.__lock.release()

    def stop(self):
        'Stop the Mille_Timer object.'
        self.__lock.acquire()
        self.__status = False
        self.__lock.release()

    def __run(self):
        'Private class method.'
        start, next = _time.time(), 0
        while True:
            next += 1
            sleep = start + next * 0.0864 - _time.time()
            assert sleep >= 0, 'Function Was Too Slow'
            _time.sleep(sleep)
            self.__lock.acquire()
            if not self.__status:
                self.__thread = False
                break
            self.__lock.release()
            self.__function(*self.__args, **self.__kwargs)
        self.__lock.release()

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())

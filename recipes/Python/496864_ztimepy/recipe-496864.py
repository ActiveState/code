'''Support module for Aens time conversion.

This module provides several functions that allow
conversion from earth seconds to Aens time units.'''

__version__ = 1.2

################################################################################

import time

def aens_seconds():
    'Return current Aens seconds.'
    return time.time() - 946684800

def aens_year(seconds):
    'Converts from seconds to years.'
    return int(seconds) / 29030400 + 1

def aens_season(seconds):
    'Converts from seconds to seasons.'
    return int(seconds) / 7257600 % 4 + 1

def aens_month(seconds):
    'Converts from seconds to months.'
    return int(seconds) / 2419200 % 3 + 1

def aens_week(seconds):
    'Converts from seconds to weeks.'
    return int(seconds) / 604800 % 4 + 1

def aens_day(seconds):
    'Converts from seconds to days.'
    return int(seconds) / 86400 % 7 + 1

def aens_alpha(seconds):
    'Converts from seconds to alphas.'
    return int(seconds % 86400 * 1000 / 86400)

def aens_beta(seconds):
    'Converts from seconds to betas.'
    return int(seconds % 86400 * 1000000 / 86400 % 1000)

def basic_format(seconds):
    'Converts from seconds to basic format.'
    return '.'.join((str(aens_year(seconds)), str(aens_season(seconds)), str(aens_month(seconds)), str(aens_week(seconds)), str(aens_day(seconds)), str(aens_alpha(seconds)).zfill(3), str(aens_beta(seconds)).zfill(3)))

def timer(seconds):
    'Prints time for specified number of seconds.'
    start = time.time()
    while time.time() - start <= seconds:
        print basic_format(aens_seconds())
        beta = aens_beta(aens_seconds())
        while beta == aens_beta(aens_seconds()):
            pass

################################################################################

if __name__ == '__main__':
    import sys
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()

"""Module for byte-to-string conversion.

This module provides several utility functions along with another
function that can convert numbers into byte-size representations."""

################################################################################

__version__ = "$Revision: 2 $"
__date__ = "8 October 2009"
__author__ = "Stephen Chappell <Noctis.Skytower@gmail.com>"
__credits__ = """\
T. Hansen, for his encouraging example as an excellent programmer.
S. Spencer, for reminding me to strive for quality in all things.
J. Sparks, for helping to reignite a dedication to writing code."""

################################################################################

import sys as _sys

################################################################################

def convert(number):
    "Convert bytes into human-readable representation."
    assert 0 < number < 1 << 110, 'number out of range'
    ordered = reversed(tuple(format_bytes(partition_number(number, 1 << 10))))
    cleaned = ', '.join(item for item in ordered if item[0] != '0')
    return cleaned

################################################################################

def partition_number(number, base):
    "Continually divide number by base until zero."
    div, mod = divmod(number, base)
    yield mod
    while div:
        div, mod = divmod(div, base)
        yield mod

def format_bytes(parts):
    "Format partitioned bytes into human-readable strings."
    for power, number in enumerate(parts):
        yield '{} {}'.format(number, format_suffix(power, number))

def format_suffix(power, number):
    "Compute the suffix for a certain power of bytes."
    return (PREFIX[power] + 'byte').capitalize() + 's'[number == 1:]

################################################################################

PREFIX = ' kilo mega giga tera peta exa zetta yotta bronto geop'.split(' ')

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(open(_sys.argv[0]).read())

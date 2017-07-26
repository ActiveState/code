"""Prints full name of all occurrences of given filename in your PATH.

Usage: findinpath.py filename"""

import os
import sys

def main():
    if len(sys.argv) < 2:
        print __doc__
        return 2
    filename = sys.argv[1]

    status = 1
    sep = ';' if sys.platform == 'win32' else ':'

    for path in os.environ['PATH'].split(sep):
        fullname = os.path.join(path, filename)
        if os.path.exists(fullname):
            print fullname
            status = 0

    return status

if __name__ == '__main__':
    sys.exit(main())

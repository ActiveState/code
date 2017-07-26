#!/usr/bin/env python
"""interleave.py <glob1> [, <glob1> ... ]

Accepts one of more files or globs interleaving lines and writing to stdout.

"""
import os
import sys
import glob

def iter_interleave(*iterables):
    """
    A generator that interleaves the output from a one or more iterators
    until they are *all* exhausted.

    """
    iterables = map(iter, iterables)
    while iterables:
        result = []
        for it in iterables:
            try:
                result.append(it.next())
            except StopIteration:
                iterables.remove(it)
        print result
        for item in result:
            yield item

if __name__ == '__main__':
    files = []

    if len(sys.argv) < 2:
        print __doc__.split("\n")[0]
        sys.exit(1)

    if sys.argv[1].lower() in ('-h', '--help'):
        print __doc__,
        sys.exit(0)

    for arg in sys.argv[1:]:
        for entry in glob.glob(arg):
            if os.path.isfile(entry):
                files.append(open(entry, 'U')) # Use universal newline support

    for line in iter_interleave(*files):
        print line,

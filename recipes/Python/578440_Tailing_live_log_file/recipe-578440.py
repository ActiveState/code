#!/usr/bin/python2.7
# vim:ai:et:ts=4:sw=4:wm=0:encoding=utf8:fileencoding=utf8
"""
tail.py
=======
Exports 'follow', which yields linewise the content being added
to a text file, similar to unix' "tail -f" functionality.

As a demonstration, you can run this script directly with an
argument, the filename you wish to follow. I use it to follow
my httpd logs:

$ python2.7 tail.py /var/log/httpd/access_log
....

"""

__all__ = ('follow',)

import time

def follow(stream):
    "Follow the live contents of a text file."
    line = ''
    for block in iter(lambda:stream.read(1024), None):
        if '\n' in block:
            # Only enter this block if we have at least one line to yield.
            # The +[''] part is to catch the corner case of when a block
            # ends in a newline, in which case it would repeat a line.
            for line in (line+block).splitlines(True)+['']:
                if line.endswith('\n'):
                    yield line
            # When exiting the for loop, 'line' has any remaninig text.
        elif not block:
            # Wait for data.
            time.sleep(1.0)
    # The End.

if __name__ == '__main__':
    # As a simple demonstration, run it with the filename to tail.
    import sys
    with open(sys.argv[1], 'rt') as following:
        following.seek(-64, 2)
        try:
            for line in follow(following):
                sys.stdout.write(line)
        except KeyboardInterrupt:
            pass

# Fin.

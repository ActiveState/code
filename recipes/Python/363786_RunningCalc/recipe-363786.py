#!/usr/bin/env python

"""This is a trivial calculator "shell" with a running total."""

import sys


current = 0.0
while True:
    sys.stdout.write("$ %s" % current)
    try:
        current = eval(str(current) + raw_input())
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
    except Exception, e:
	sys.stderr.write("Error: %s\n" % e)

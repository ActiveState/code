from sys import version_info as version

if version.major == 2:
    range = xrange

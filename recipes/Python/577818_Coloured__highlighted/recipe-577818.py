#!/usr/bin/env python

"""
Print an highlighted version of string (POSIX only).

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT
"""

import sys


def _term_supports_colors(file=sys.stdout):
    try:
        import curses
        assert file.isatty()
        curses.setupterm()
        assert curses.tigetnum("colors") > 0
    except Exception:
        return False
    else:
        return True


if _term_supports_colors():
    def hilite(string, ok=True, bold=False):
        """Return an highlighted version of 'string'."""
        attr = []
        if ok is None:  # no color
            pass
        elif ok:   # green
            attr.append('32')
        else:   # red
            attr.append('31')
        if bold:
            attr.append('1')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
else:
    hilite = lambda s, *args, **kwargs: s


if __name__ == '__main__':
    print hilite('hello')
    print hilite('hello', ok=False)
    print hilite('hello', ok=True, bold=True)
    print hilite('hello', ok=False, bold=True)
    print hilite('hello', ok=None, bold=False)
    print hilite('hello', ok=None, bold=True)

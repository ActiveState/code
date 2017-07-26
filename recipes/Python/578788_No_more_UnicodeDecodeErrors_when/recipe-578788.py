"""Module to avoid UnicodeDecodeErrors when printing."""

# tostdout.py by Ádám Szieberth (2013)
# Python 3.3

# Full license text:
# --------------------------------------------------------------
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or
# modified copiesof this license document, and changing it is
# allowed as long as the name is changed.
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND
# MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
# --------------------------------------------------------------

import sys

ENCODING = sys.stdout.encoding
ERRORS = "replace"

def to_stdout(string, errors=ERRORS):
    """
    Converts a string to stdout-compatible encoding. This helps
    to avoid getting UnicodeDecodeError exceptions for print
    calls.
    """
    encoded = string.encode(ENCODING, errors)
    decoded = encoded.decode(ENCODING)
    return decoded

def print2(*objs, errors=ERRORS):
    """
    You will not get UnicodeDecodeError exceptions when you use
    this function instead of the builtin print().
    """
    print(*(to_stdout(str(o), errors) for o in objs))

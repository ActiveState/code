# WARNING: This recipe currently breaks display of the representation of strings containing other string escape sequences such as '\n'. I can't find a way to get ASPN to hide the recipe from public view until I can figure out a way to fix it though :(

# NOTE: This recipe is written to work with Python 3.0
# It would likely require changes to work on Python 2.6, and won't work at all
# on earlier 2.x versions

import sys, io

# With the new IO module, it's easy to create a variant of an
# existing IO class
class ParseUnicodeEscapes(io.TextIOWrapper):
  def write(self, text):
    super().write(text.encode('latin-1').decode('unicode_escape'))

# To replace sys.stdout/stderr, we first collect the necessary
# constructor arguments from the current streams

stdout_args = (sys.stdout.buffer, sys.stdout.encoding, sys.stdout.errors,
               None, sys.stdout.line_buffering)
stderr_args = (sys.stderr.buffer, sys.stderr.encoding, sys.stderr.errors,
               None, sys.stderr.line_buffering)

# Once we replace the streams, any '\uXXXX' sequences written to
# sys.stdout or sys.stderr will be replaced with the corresponding
# Unicode characters
sys.stdout = ParseUnicodeEscapes(*stdout_args)
sys.stderr = ParseUnicodeEscapes(*stderr_args)

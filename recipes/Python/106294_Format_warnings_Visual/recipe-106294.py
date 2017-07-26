# Put this code in your script.
#
# It uses the standard Python warnings framework,
# and installs a custom warning message formatter that
# generates messages Visual Studio will understand.

import warnings
from warnings import warn

def my_formatwarning(message, category, filename, lineno):
    """ Return a warning message, formatted for Visual Studio """
    return "%s(%i) : warning: %s" % (filename, lineno, message)

# Replace default warning formatter with custom formatter
warnings.formatwarning = my_formatwarning



# Now for some sample code that generates warnings.
# Your code can call warn() anywhere.
def foo():
    warn("You called foo(); don't do that")

foo()

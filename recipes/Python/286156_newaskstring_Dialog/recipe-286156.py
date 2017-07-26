# 11-06-04
#v1.0.0

# newaskstring
# A *slightly* modified askstring function from the tkSimpleDialog module by Frederik Lundh
# Allows a default value to be supplied.

# Copyright Michael Foord
# Not for use in commercial projects without permission. (Although permission will probably be given).
# If you use in a non-commercial project then please credit me and include a link back.
# If you release the project then let me know (and include this message with my code !)

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail or michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html

from tkSimpleDialog import _QueryString

def askstring(title, prompt, default=None, **kw):
    '''get a string from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        default -- the initial text to display
        **kw -- see SimpleDialog class

    Return value is a string
    '''
    d = _QueryString(title, prompt, default, **kw)
    return d.result

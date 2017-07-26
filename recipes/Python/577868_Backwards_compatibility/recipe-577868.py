# compatibility.py
#

# Backwards compatibility for text mode Python 1.4.0 to 3.2.2...

# Some simple lines that work for all these versions on the

# classic AMIGA, E-UAE, PCLinuxOS 2009, Debian 6.0.0, Windows XP and

# Vista and WinUAE. Note, classic AMIGAs and derivatives only reach

# Python version 2.4.6. AROS goes to version 2.5.2.

# Python versions checked against, 1.4.0, 2.0.1, 2.4.2, 2.5.2, 2.6.1

# 2.6.6, 2.7.2, 3.0.1, 3.1.3 and 3.2.2.

# These are to go along with this pointer...

# http://code.activestate.com/recipes/577836-raw_input-for-all-versions-of-python/?in=lang-python

# ===================================================================

# A method for generating a filename automatically and in this case

# adding an extension .DAT. The higher the number the "newer" the

# filename. Simple and easy to do.

import time

# Allocate default values.

autofilename="0000000000.DAT"

n=int(time.time())

# Now generate the automatic filename.

autofilename=str(n)

autofilename=autofilename+".DAT"

# Just print to the screen as proof of the working example.

print(autofilename)

# ===================================================================

# ===================================================================

# Some ASCII print statements that work for general usage...

# These all look the same on screen whatever the version or platform

# above. These print two newlines.

print("")

print('')

# These are a simple basic "ECHO sometext" command.

print("This method can be used thoughout as a basic ECHO to the screen.")

print('This method can be used thoughout as a basic ECHO to the screen.')

# Now a print statement that uses a variable called "texttest".

# The bell character assumes that the audio is enabled in all the

# platforms above, otherwise it is ignored...

texttest="\n\nSometext to print to the screen...\a\b\b Overwrite two of the full stops."

print(texttest)

texttest='Single quotes with escape characters.\rMaybe the start of this line will be overwritten, see the code... ;o)'

print(texttest)

# ===================================================================

# Regular expressions DO NOT work nor print statements/functions with

# variables inside.

# There will be more to come.

# Enjoy finding simple solutions to often very difficult problems.

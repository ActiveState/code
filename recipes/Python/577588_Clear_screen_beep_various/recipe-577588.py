# Clear-screen and error beep module for various platforms.

# ---------------------------------------------------------

#

# File saved as "clsbeep.py" and placed into the Python - Lib drawer or
# where-ever the modules are located.

#

# Setting up a basic error beep and clear screen for Python 1.4 and greater.

# (Original idea copyright, (C)2002, B.Walker, G0LCU.)

#

# Issued as Public Domain and you can do with it as you please.

#

# Tested on Python 1.4.x for a stock AMIGA 1200 and Python 2.0.x for WinUAE.

# Tested on Python 2.4.2 for Windows ME and Python 2.6.2 for XP-SP2.

# (Now changed to include Windows Vista, [and Windows 7?], to Python 2.7.x)

# Tested on Python 2.5.2 for PCLinuxOS 2009, Knoppix 5.1.1 and Python 2.6.6

# on Debian 6.0.0...
# All platforms in CLI/Command-Prompt/Terminal mode.

#

# It is SO easy to convert to Python 3.x that I have not bothered. I`ll leave

# you guys to work that one out... :)

#

# ----------------------

# Usage in other files:-

# >>> import clsbeep[RETURN/ENTER]

# ----------------------

# Called as:-

# clsbeep.beep()

# clsbeep.cls()

# clsbeep.both()

# ----------------------

# The ~if~ statement selects the correct format for the platform in use.

# ----------------------



# Import necessary modules for this to work.

import os

import sys



# Generate a beep when called.

def beep():

	# A stock AMIGA 1200 using Python 1.4 or greater.

	# This assumes that the sound is enabled in the PREFS: drawer.

	# AND/OR the screen flash is enabled also.

	if sys.platform=='amiga':

		print '\a\v'



	# MS Windows (TM), from Windows ME upwards. Used in Command

	# Prompt mode for best effect.

	# The *.WAV file can be anything of your choice.

	# CHORD.WAV was the default.

	# SNDREC32.EXE no longer exists in WIndows Vista, and higher?

	if sys.platform=='win32':

		# os.system('SNDREC32.EXE "C:\WINDOWS\MEDIA\CHORD.WAV" /EMBEDDING /PLAY /CLOSE')

		print chr(7),



	# A generic error beep for all Linux platforms.

	# There is a simple way to change the frequency, and the amplitude.

	# This also works in a Linux terminal running a Python interpreter!

	if sys.platform=='linux2':

		audio=file('/dev/audio', 'wb')

		count=0

		while count<250:

			beep=chr(63)+chr(63)+chr(63)+chr(63)

			audio.write(beep)

			beep=chr(0)+chr(0)+chr(0)+chr(0)

			audio.write(beep)

			count=count+1

		audio.close()



	# Add here for other OSs.

	# Add here any peculiarities.

	# if sys.platform=='some-platform':

		# Do some sound error beep.



# Do a clear screen, with the limitations as shown.

def cls():

	# A stock AMIGA 1200 using Python 1.4 or greater.

	if sys.platform=='amiga':

		print '\f',



	# MS Windows (TM), from Windows ME upwards.

	# This is for the Command Prompt version ONLY both windowed AND/OR

	# screen modes.

	if sys.platform=='win32':

		print os.system("CLS"),chr(13)," ",chr(13),



	# A generic version for all Linux platforms.

	# For general console Python usage.

	if sys.platform=='linux2':

		print os.system("clear"),chr(13)," ",chr(13),



	# Add here for other OSs.

	# Peculiarities here.

	# if sys.platform=='some-platform':

		# Do some clear screen action...



# Do both if required.

def both():

	beep()

	cls()



# Module end...
# Enjoy finding simple solutions to often very difficult problems.

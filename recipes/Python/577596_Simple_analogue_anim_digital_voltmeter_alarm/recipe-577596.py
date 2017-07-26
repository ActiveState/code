# DO NOT TAKE THIS EXAMPLE TO SERIOUSLY... :)
#
# A demo analogue and digital readout using standard Python Version 1.4.x
# for a classic AMIGA A1200, Version 2.4.x for Windows ME to Vista+ and
# Version 2.5.2 for Linux. Used in CLI/Command-Prompt/Terminal mode.
# I do have a Python 3.x.x version and will upload that later... :o)
#
# This uses an experimental module that clears the screen and generates a
# beep on platforms AMIGA, MS-DOS window or screen using MS Windows ME to
# Vista and Linux using Kernel 2.4+...
# It can be found here:-
# http://code.activestate.com/recipes/577588-clear-screen-and-beep-for-various-platforms/?in=lang-python
#
# (Original copyright, (C)2006, B.Walker, G0LCU.)
# Now issued as Public Domain, you may do with it as you please.

# Import necessary modules for this demo.
import random
import time

# This is the experimental module.
import clsbeep

# Use this experimental clear screen module to clear the screen.
clsbeep.cls()

# The main working code.
def main():
	# Set up variables as global... ;o)
	global mybyte
	global digital
	global analogue
	global n

	# Allocate definite values.
	mybyte = 0
	digital = 0
	analogue = 0
	n = 0

	while 1:
		# Generate a byte number as though taken from _a_ serial, parallel or USB port.
		# I will upload simple standard Python code to access HW in the near future... :)
		mybyte = int(random.random() * 256)

		# Convert to a value to look like a 5.10V "FS" on the digital readout.
		digital = mybyte * 0.02

		# Set up a working display.
		print
		print '          Analogue and digital demo readout for simple animation test.'
		print
		print '                                   +--------+'
		print '                                     ',digital
		print '                                   +--------+'
		print

		# Convert to some sort of analogue look, 6 bit depth.
		analogue = (mybyte/5)

		print
		print '    Scale.    0   0.5  1.0  1.5  2.0  2.5  3.0  3.5  4.0  4.5  5.0'
		print '              ++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print '              ',
		# Do the simple animation for the analogue look.
		n = 0
		while n <= analogue:
			print '\b|',
			n = n + 1
		print
		print '              +----+----+----+----+----+----+----+----+----+----+-'

		# Generate an "OVERLOAD" beep when above a preselected value...
		# In this case anything above "4.02" will generate an error beep.
		if digital >= 4.02:
			clsbeep.beep()

		# Hold for about 1 second.
		# Not needed when proper HW is connected, but IS needed for this demo.
		time.sleep(1)

		# Clear the screen for a re-run.
		clsbeep.cls()
main()

# End of demo.
# Enjoy finding simple solutions to often very difficult problems.

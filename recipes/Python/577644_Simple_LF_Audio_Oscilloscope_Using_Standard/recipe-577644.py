#!/usr/bin/python
#
# AudioScope.py
#
# DEMO LF Audio Oscilloscope using /dev/dsp inside Linux.
# Original copyright, (C)2011, B.Walker, G0LCU.
# Initially issued to LXF under the MIT licence.
#
# The timebase runs vertically and the waveform amplitude horizontally.
# It grabs a sample for about 1 second and displays the results AFTER
# the sample; technically a basic LF Storage Audio Oscilloscope.
# 
# The display only uses standard ASCII characters.
#
# To run just type from the prompt ">>>"...
# >>> execfile("/full/path/to/AudioScope.py")<RETURN/ENTER>
#
# Tested on Python 2.6.x only but should work on other versions of 2.x.x.
# Ensure /dev/dsp exists; if not install oss-compat from your distro`s
# repository. Also ensure the sound card is not already in use.
#
# Enjoy finding simple solutions to often very difficult problems... ;o)
#
# If you are just trying this out and have an internal mic, just talk
# loudly into the microphone and see your vocal wavefrom on screen...
# Needless to say using the external microphone input as an input this
# becomes a single channel uncalibrated LF Audio Oscilloscope.
#
# Press Ctrl-C to STOP.

# Import any necessary modules.
import os

# Do a basic screen clear. 
os.system("clear")
# Turn the cursor off to look prettier... ;o)
os.system("setterm -cursor off")

def main():
	# Set special variables global.
	global audioscope
	global chardisplay
	global offset
	global timebase
	global record

	# Known variables.
	audioscope = 0
	chardisplay = "(C)2011, B.Walker, G0LCU."
	offset = 0
	timebase = 1
	record = "Initial issue to LXF under the MIT licence"
	
	# Throw away local variables.
	n = 0

	while 1:
		# Sample the microphone/external_microphone_input for approximately 1 second.
		audio = file('/dev/dsp', 'rb')
		record = audio.read(8192)
		audio.close()

		# This value points to a character in the 8192 byte string.
		# "offset" can be any value from 0 to 191.
		offset = 0
		# Start the loop from character at position 0.
		while offset <= 8191:
			# Convert the character to a decimal number.
			audioscope = ord(record[offset])
			# Now convert to 6 bit depth to fit one terminal line.
			audioscope = int(audioscope/4)
			# This should never occur but don`t allow an error.
			if audioscope >= 63: audioscope = 63
			if audioscope <= 0: audioscope = 0
			# Invert to correct the trace shown.
			audioscope = 63 - audioscope

			# Loop count to get the correct position to print the plot.
			n = 0
			# Set the trace position for each line and......
			chardisplay = "       "
			while n <= audioscope:
				# ......add the required spaces until completed then......
				chardisplay = chardisplay + " "
				n = n + 1
			# ......print the plot point using *.
			print chardisplay + "*"
			# Point to the next character to character in the 8192 string.
			# "timebase" can be any value from 1 to 360.
			offset = offset + timebase

	# Assuming a Ctrl-C arrives here enable the cursor again.
	os.system("setterm -cursor off")

main()

# End of DEMO.
# Enjoy finding simple solutions to often very difficult problems.

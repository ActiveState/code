# A stereo "White Noise" generator using STANDARD Python 2.5.2 or higher.
# This is for (PC)Linux(OS), (ONLY?), and was done purely for fun.
#
# It is another simple piece of testgear for the amateur electronics
# enthusiast and uses /dev/dsp instead of /dev/audio. Enjoy... ;o)
#
# (Original copyright, (C)2010, B.Walker, G0LCU.)
#
# DONATED TO LXF AS PUBLIC DOMAIN...
#
# Ensure the sound is enabled and the volume is turned up.
#
# Copy the file to the Lib folder/drawer/directory where Python resides,
# or where the modules reside, as "noise.py" without the quotes.
#
# Start the Python interpreter from a console/terminal window.
#
# For a quick way to run the noise generator just use at the ">>>" prompt:-
#
# >>> import noise[RETURN/ENTER]
#
# And away we go...
#
# This code is now Public Domain and you may do with it as you please...
#
# Coded on a(n) HP dual core notebook running PCLinuxOS 2009 and
# Python 2.5.2 for Linux; also tested on Knoppix 5.1.1 and Python 2.5.2
# and Debian 6.0.0 and Python 2.6.6...
#
# Connect an oscilloscope to the earphone socket(s) to see the noise
# waveform(s) being generated.

# Import any modules...
import os
import random

# Clear a terminal window ready to run this program.
print os.system("clear"),chr(13),"  ",chr(13),

# The program proper...
def main():
	# Make all variables global, a quirk of mine... :)
	global noise
	global value
	global select
	global count
	global amplitudestring
	global amplitude
	
	# The INITIAL default values.
	select="G0LCU."
	value=0
	noise=chr(value)
	count=0
	amplitudestring="64"
	amplitude=64
	
	# A continuous loop to re-generate noise as required...
	while 1:
		# Set up a basic user window.
		print os.system("clear"),chr(13),"  ",chr(13),
		print
		print "Simple Noise Generator using STANDARD Python 2.5.2"
		print "for PCLinuxOS 2009, issued as Public Domain to LXF."
		print
		print "(Original copyright, (C)2010, B.Walker, G0LCU.)"
		print
		# Set amplitude level from 0 to 64 unclusive.
		amplitudestring=raw_input("Enter amplitude level, 1 to 64:- ")
		# Don`t allow any typo error at all within limits...
		# On any typo error set amplitude to maximum.
		if amplitudestring=="": amplitudestring="64"
		if amplitudestring.isdigit()==0: amplitudestring="64"
		if len(amplitudestring)>=3: amplitudestring="64"
		# Now allocate the numerical value once the error chacking has been done.
		amplitude=int(amplitudestring)
		if amplitude<=1: amplitude=1
		if amplitude>=64: amplitude=64
		print
		# Select RETURN/ENTER for "White Noise", OR, any other key then RETURN/ENTER to Quit.
		select=raw_input("Press RETURN/ENTER for noise or any other key then RETURN/ENTER to Quit:- ")
		if select!="": break
		print os.system("clear"),chr(13),"  ",chr(13),
		print
		print "A 10 second white noise audio burst..."
		print
		print "Amplitude level",amplitude,"\b..."
		print
		# Change the random seed value per run.
		random.seed(None)
		# Open up the audio channel(s) to write directly to.
		# Note this DEMO uses /dev/dsp and NOT /dev/audo... ;o)
		audio=file('/dev/dsp','wb')
		# A count of 70000 is about 10 seconds of noise burst...
		count=0
		while count<70000:
			# Generate a random byte value.
			value=random.random()*amplitude
			noise=chr(int(value))
			# Write the character, (byte), "value" to the audio device.
			audio.write(noise)
			count=count+1
		# Close the audio device when finished.
		audio.close()
main()

# End of demo...
# Enjoy finding simple solutions to often very difficult problems...

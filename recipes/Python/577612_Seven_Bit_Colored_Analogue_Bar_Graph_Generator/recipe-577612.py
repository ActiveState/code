# SevenBitBargraph2x.py
#
# A DEMO 7 bit analogue bargraph generator in colour for STANDARD Python 2.6.x and Linux...
#
# (Original copyright, (C)2010, B.Walker, G0LCU.)
# A Python 3.x version can be found here:-
# http://www.linuxformat.com/forums/viewtopic.php?t=13443
#
# Saved as SevenBitBargraph2x.py wherever you like.
#
# This DEMO goes from safe green, to warning amber, to danger red, with a crirical
# error beep above 120 on the horizontal scale...
#
# Two system commands are required, "clear" and "setterm", for this to work.
# I assume that these are available on all recent and current Linux distros.
# The device /dev/audio is used so this must be free also. 
#
# It is useful for quick glance readings from say an 8 bit ADC used as a simple
# voltmeter, etc. Getting a digital readout is SO simple I left it out this time...
#
# To run use the following from inside a Python prompt...
# >>> exec(open("/full/path/to/code/SevenBitBargraph2x.py").read())
# OR...
# >>> execfile("/full/path/to/code/SevenBitBargraph2x.py").read()
# Tested on Debian 6.0.0 with Python 2.6.6.

# Add the required imports for this DEMO.
import os
import random
import time

def main():

	# For this DEMO set up variables as global...
	global column
	global count
	global bargraph
	
	column=0
	count=2
	bargraph="(C)2010, B.Walker, G0CLU. Now Public Domain"
	
	# Disable the cursor as it looks much nicer... ;o)
	os.system("setterm -cursor off")

	while 1:
		# Do a full, clean, clear screen and start looping.
		print os.system("clear"),unichr(13),"  ",unichr(13),

		# Set to terminal default colour(s).
		print "\033[0mSeven Bit Level Horizontal Analogue Bar Graph Display..."
		print
		print "Original copyright, (C)2010, B.Walker, G0LCU."
		print
		print "Issued to all as Public Domain."
		print
		print
		# Set the bargraph to light green for this DEMO.
		# This is equivalent to 0 for the column value.
		bargraph="        \033[1;32m|"

		# Generate a byte value as though grabbed from a serial, parallel or USB port.
		column=int(random.random()*256)
		# Now divide by 2 to simulate a 7 bit value.
		column=int(column/2)
		# Although this should never occur, don't allow any error.
		if column>=127: column=127
		if column<=0: column=0
		
		# Now to generate the bargraph...
		count=0
		while count<=column:
			# It is equivalent to BIOS character 222 for column value of 1 ONLY.
			if count==1: bargraph="        \033[1;32m"+unichr(0x2590)
			count=count+1
			if count>=2:
				while count<=column:
					# Change bargraph colour on the fly when entering the YELLOW zone... :)
					if count>=90: bargraph=bargraph+"\033[1;33m"
					# Change bargraph colour on the fly when entering the RED zone... :)
					if count>=100: bargraph=bargraph+"\033[1;31m"
					if count%2==0:
						# For every odd column value print this BIOS character 221.
						bargraph=bargraph+unichr(0x258c)
					if count%2==1:
						# For every even column value OVERWRITE the above with BIOS character 219.
						bargraph=bargraph+"\b"+unichr(0x2588)
					count=count+1
		# Print the "scale" in the default colour(s)...
		print "\033[0m        0   10   20   30   40   50   60   70   80   90   100  110  120"
		# Now print the meter and bargraph in colours of your choice... :)
		print "\033[1;32m        |    |    |    |    |    |    |    |    |    \033[1;33m|    \033[1;31m|    |    |"
		print "\033[1;32m        +++++++++++++++++++++++++++++++++++++++++++++\033[1;33m+++++\033[1;31m+++++++++++++++"
		print bargraph
		print "\033[1;32m        +++++++++++++++++++++++++++++++++++++++++++++\033[1;33m+++++\033[1;31m+++++++++++++++"
		print
		print "           \033[1;34m  Analogue resolution is half of one division, that is 1."
		print
		# Return back to the default colours and for this DEMO the column value...
		print "\033[0mColumn number",column,"\b...     "
		print
		print "Press Ctrl-C to stop..."

		# Do a critical error beep, [sine wave(ish)] for about 1second.
		if column>=120:
			# Set up the binary code as a crude sinewave.
			waveform=b"\x0f\x2d\x3f\x2d\x0f\x03\x00\x03"
			# Set audio timing to zero, "0".
			count=0
			# Open up the audio device to write to.
			# This could be /dev/dsp also...
			audio=open("/dev/audio", "wb")
			# A "count" value of 1 = 1mS, so 1000 = 1S.
			while count<=1000:
				# Send 8 bytes of data to the audio device 1000 times.
				# This is VERY close to 1KHz and almost sinewave.
				audio.write(waveform)
				count=count+1
			# Close the audio device access.
			audio.close()

		# Add a DEMO delay to simulate a simple digital voltmeter speed...
		if column<=119: time.sleep(1)
	
	# Enable the cursor again if it ever gets here... ;oO
	os.system("setterm -cursor on")
main()

# DEMO end.
# Enjoy finding simple solutions to often very difficult problems...

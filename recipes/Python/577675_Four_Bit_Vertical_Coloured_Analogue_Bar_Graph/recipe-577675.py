# 4BitVerticalBargraph2x.py
#
# A DEMO 4 bit slow analogue bargraph generator in colour for STANDARD Python 2.6.x and Linux...
# This is a vertical version of the horizontal one also given away by myself.
# It is written so that anyone can understand how it works.
#
# (Original copyright, (C)2011, B.Walker, G0LCU.)
# Issued initially to LXF as Public Domain, and to other sites later.
#
# Saved as 4BitVerticalBargraph2x.py wherever you like.
#
# This DEMO goes from safe green, to warning amber, to danger red, with a crirical
# error beep above 14 on the vertical scale...
# It is a slow "AT A GLANCE" display for quick assessments, not for accuracy.
#
# Two system commands are required, "clear" and "setterm", for this to work.
# I assume that these are available on all recent and current Linux distros.
# The device /dev/audio is used so this must be free also. 
#
# It is useful for quick "AT A GLANCE" readings from say an 8 bit ADC used as a simple
# voltmeter, ammeter, etc. Getting a digital readout is SO simple I left it out this time...
#
# To run use the following from inside a Python prompt...
# >>> exec(open("/full/path/to/code/4BitVerticalBargraph2x.py").read())
# OR...
# >>> execfile("/full/path/to/code/4BitVerticalBargraph2x.py")
#
# This looks like an "LED" style "VU" display...

# Add the required imports for this DEMO.
import os
import random
import time

# Just for this DEMO set up variables as global...
global count
global row
global blank
global greenlines
global yellowlines
global redlines
global waveform

# Startup variable values here.
count=0
row=0
blank="(C)2011, B.Walker, G0LCU."
greenlines=blank
yellowlines=blank
redlines=blank
# This is a square wave binary for the critical error beep.
waveform=chr(15)+chr(45)+chr(63)+chr(45)+chr(15)+chr(3)+chr(0)+chr(3)

def main():
	# Disable the cursor as it looks much nicer... ;o)
	os.system("setterm -cursor off")

	while 1:
		# Run continuously and use Ctrl-C to STOP!
		count=15
		blank="\033[0m                                 "
		# Generate a byte value as though grabbed from a serial, parallel or USB port.
		row=int(random.random()*256)
		# Now divide by 16 to simulate a 4 bit value.
		row=int(row/16)
		# Although this should never occur, don't allow any error.
		if row>=15: row=15
		if row<=0: row=0

		while count>=0:
			# Do a full, clean, clear screen and start looping.
			os.system("clear"),chr(13),"  ",chr(13),
			print "\033[0mFour Bit Level Vertical Analogue Bar Graph Display..."
			print "Original copyright, (C)2011, B.Walker, G0LCU."
			print "Issued to LXF on 24-04-2011 as Public Domain."
			print
			print blank+"\033[1;31m15 __ "
			
			redlines=blank+"\033[1;31m14 __ "
			if row>=15: redlines=redlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print redlines

			redlines=blank+"\033[1;31m13 __ "
			if row>=14: redlines=redlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print redlines

			yellowlines=blank+"\033[1;33m12 __ "
			if row>=13: yellowlines=yellowlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print yellowlines

			yellowlines=blank+"\033[1;33m11 __ "
			if row>=12: yellowlines=yellowlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print yellowlines

			yellowlines=blank+"\033[1;33m10 __ "
			if row>=11: yellowlines=yellowlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print yellowlines

			greenlines=blank+"\033[1;32m 9 __ "
			if row>=10: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 8 __ "
			if row>=9: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 7 __ "
			if row>=8: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 6 __ "
			if row>=7: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 5 __ "
			if row>=6: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 4 __ "
			if row>=5: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 3 __ "
			if row>=4: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 2 __ "
			if row>=3: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines

			greenlines=blank+"\033[1;32m 1 __ "
			if row>=2: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			print greenlines
			
			greenlines=blank+"\033[1;32m 0 __ "
			if row>=1: greenlines=greenlines+unichr(0x2588)+unichr(0x2588)
			count=count-1
			if row==0: greenlines=greenlines+"__"
			count=count-1
			print greenlines
			
			# Reset to default colours...
			print
			print "\033[0mPress Ctrl-C to stop..."

		if row<=14: time.sleep(1)
		if row==15:
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
			
	# Enable the cursor again if it ever gets here... ;oO
	os.system("setterm -cursor on")
main()

# End of DEMO...
# Enjoy finding simple solutions to often very difficult problems...

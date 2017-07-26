# Dual4BitVerticalBargraph3x.py
#
# A DEMO DUAL 4 bit slow analogue bargraph generator in colour for STANDARD Python 3.x.x
# and Linux... This is a DUAL vertical version of the SINGLE one also given away by myself.
# It is written so that anyone can understand how it works.
#
# (Original copyright, (C)2011, B.Walker, G0LCU.)
#
# Saved as Dual4BitVerticalBargraph3x.py wherever you like.
#
# This DEMO goes from safe green, to warning amber, to danger red, with a crirical
# error beep above 14 on both the vertical displays...
# It is a slow "AT A GLANCE" display for quick assessments, not for accuracy.
#
# Two system commands are required, "clear" and "setterm", for this to work.
# I assume that these are available on all recent and current Linux distros.
# The device /dev/audio is used so this must be free also. 
#
# It is useful for quick "AT A GLANCE" readings from say two 8 bit ADCs used as a simple
# voltmeters, ammeters, etc...
#
# To run use the following from inside a Python prompt...
# >>> exec(open("/full/path/to/code/Dual4BitVerticalBargraph3x.py").read())
#
# This looks like two "LED" style "VU" displays side by side...

# Add the required imports for this DEMO.
import os
import random
import time

# Just for this DEMO set up variables as global...
global count
global byteone
global bytetwo
global blank
global greenlines
global yellowlines
global redlines
global waveform
global unichar
global spacer

# Startup variable values here.
count=0
byteone=0
bytetwo=0
blank="(C)2011, B.Walker, G0LCU."
greenlines=blank
yellowlines=blank
redlines=blank
unichar=chr(0x2588)+chr(0x2588)
spacer=" ____ "
# This is a squarewave binary for the critical error beep(s).
waveform=b"\x00\x00\x00\x00\xff\xff\xff\xff"

def main():
	# Disable the cursor as it looks much nicer... ;o)
	os.system("setterm -cursor off")

	while 1:
		# Run continuously and use Ctrl-C to STOP!
		blank="\033[0m                              "
		# Generate two byte values as though grabbed from a serial, parallel or USB port.
		# E.G... The Arduino Diecimila Dev Board as a multiple analogue source.
		byteone=int(random.random()*256)
		bytetwo=int(random.random()*256)
		# Now divide by 16 to simulate a 4 bit values.
		byteone=int(byteone/16)
		bytetwo=int(bytetwo/16)
		# Although this should never occur, don't allow any errors.
		if byteone>=15: byteone=15
		if byteone<=0: byteone=0
		if bytetwo>=15: bytetwo=15
		if bytetwo<=0: bytetwo=0

		# Do a full, clean, clear screen and start looping.
		os.system("clear"),chr(13),"  ",chr(13),
		print("\033[0mDual Four Bit Level Vertical Analogue Bar Graph Display...")
		print()
		print("Original copyright, (C)2011, B.Walker, G0LCU.")
		print()
		print(blank+"\033[1;31m15 __ __ ____ __ __ 15")

		redlines=blank+"\033[1;31m14 __ "
		if byteone>=15: redlines=redlines+unichar+spacer
		else: redlines=redlines+"  "+spacer
		if bytetwo>=15: redlines=redlines+unichar+" __ 14"
		else: redlines=redlines+"   __ 14"
		print(redlines)

		redlines=blank+"\033[1;31m13 __ "
		if byteone>=14: redlines=redlines+unichar+spacer
		else: redlines=redlines+"  "+spacer
		if bytetwo>=14: redlines=redlines+unichar+" __ 13"
		else: redlines=redlines+"   __ 13"
		print(redlines)

		yellowlines=blank+"\033[1;33m12 __ "
		if byteone>=13: yellowlines=yellowlines+unichar+spacer
		else: yellowlines=yellowlines+"  "+spacer
		if bytetwo>=13: yellowlines=yellowlines+unichar+" __ 12"
		else: yellowlines=yellowlines+"   __ 12"
		print(yellowlines)

		yellowlines=blank+"\033[1;33m11 __ "
		if byteone>=12: yellowlines=yellowlines+unichar+spacer
		else: yellowlines=yellowlines+"  "+spacer
		if bytetwo>=12: yellowlines=yellowlines+unichar+" __ 11"
		else: yellowlines=yellowlines+"   __ 11"
		print(yellowlines)

		yellowlines=blank+"\033[1;33m10 __ "
		if byteone>=11: yellowlines=yellowlines+unichar+spacer
		else: yellowlines=yellowlines+"  "+spacer
		if bytetwo>=11: yellowlines=yellowlines+unichar+" __ 10"
		else: yellowlines=yellowlines+"   __ 10"
		print(yellowlines)

		greenlines=blank+"\033[1;32m 9 __ "
		if byteone>=10: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=10: greenlines=greenlines+unichar+" __ 9"
		else: greenlines=greenlines+"   __ 9"
		print(greenlines)

		greenlines=blank+"\033[1;32m 8 __ "
		if byteone>=9: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=9: greenlines=greenlines+unichar+" __ 8"
		else: greenlines=greenlines+"   __ 8"
		print(greenlines)

		greenlines=blank+"\033[1;32m 7 __ "
		if byteone>=8: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=8: greenlines=greenlines+unichar+" __ 7"
		else: greenlines=greenlines+"   __ 7"
		print(greenlines)

		greenlines=blank+"\033[1;32m 6 __ "
		if byteone>=7: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=7: greenlines=greenlines+unichar+" __ 6"
		else: greenlines=greenlines+"   __ 6"
		print(greenlines)

		greenlines=blank+"\033[1;32m 5 __ "
		if byteone>=6: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=6: greenlines=greenlines+unichar+" __ 5"
		else: greenlines=greenlines+"   __ 5"
		print(greenlines)

		greenlines=blank+"\033[1;32m 4 __ "
		if byteone>=5: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=5: greenlines=greenlines+unichar+" __ 4"
		else: greenlines=greenlines+"   __ 4"
		print(greenlines)

		greenlines=blank+"\033[1;32m 3 __ "
		if byteone>=4: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=4: greenlines=greenlines+unichar+" __ 3"
		else: greenlines=greenlines+"   __ 3"
		print(greenlines)

		greenlines=blank+"\033[1;32m 2 __ "
		if byteone>=3: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=3: greenlines=greenlines+unichar+" __ 2"
		else: greenlines=greenlines+"   __ 2"
		print(greenlines)

		greenlines=blank+"\033[1;32m 1 __ "
		if byteone>=2: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"  "+spacer
		if bytetwo>=2: greenlines=greenlines+unichar+" __ 1"
		else: greenlines=greenlines+"   __ 1"
		print(greenlines)

		greenlines=blank+"\033[1;32m 0 __ "
		if byteone>=1: greenlines=greenlines+unichar+spacer
		else: greenlines=greenlines+"__"+spacer
		if bytetwo>=1: greenlines=greenlines+unichar+" __ 0"
		else: greenlines=greenlines+"__ __ 0"
		print(greenlines)

		# Print the two byte values onto the screen...
		print("\033[1;34mByteone =",byteone,"\b, bytetwo =",bytetwo,"\b...   ")
		# Now reset to the default colours, etc...
		print("\033[0mPress Ctrl-C to stop...")

		time.sleep(1)

		# Use two different beeps for the two displays.
		# Both are different frequency squarewaves.
		if byteone==15 or bytetwo==15:
			# Select an error beep for each display...
			if byteone==15: waveform=b"\x00\x00\x00\x00\xff\xff\xff\xff"
			if bytetwo==15: waveform=b"\x00\x00\xff\xff\x00\x00\xff\xff"
			# Set audio timing to zero, "0".
			count=0
			# Open up the audio device to write to.
			# This could be /dev/dsp also...
			audio=open("/dev/audio", "wb")
			# A "count" value of 1 = 1mS, so 1000 = 1S.
			while count<=1000:
				# Send 8 bytes of data to the audio device 1000 times.
				audio.write(waveform)
				count=count+1
			# Close the audio device access.
			audio.close()

	# Enable the cursor again if it ever gets here... ;oO
	os.system("setterm -cursor on")
main()

# End of DEMO...
# Enjoy finding simple solutions to often very difficult problems...

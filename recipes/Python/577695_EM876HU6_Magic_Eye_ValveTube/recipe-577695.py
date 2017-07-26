# MagicEye.py
#
# A simple animation DEMO to simulate the action of a thermionic tuning indicator valve/tube.
# The valve/tube type is EM87, 6HU6, CV10407, 6E2 and other equivalent numbers too.
# http://www.akh.se/tubes/htm/em87.htm
#
# Original copyright, (C)2011, B.Walker, G0LCU.
# 
# Save the file as MagicEye.py in the Lib and/or Modules drawer/directory/folder.
# To test from a normal Python Command Prompt/Terminal call as......
#
# >>> import MagicEye
#
# ......and away you go and enjoy... ;o)
#
# Tested on Windows Vista using Python 2.6.2 and Debian Linux using Python 2.6.6.
# Also tested on PCLinusOS 2009 using Python 2.5.2... (All are default installs.)
# This code assumes white foreground and black background colours.
#
# Written in such a way that anyone can understand how it works!
# This code CAN be simplified quite a lot but it has been left as is...
#
# It is useful for quick glance readings from say an 8 bit ADC used as a simple level
# indicator, for example a tuning and/or level indicator.
# It is at 5 bit depth.
#
# The commands, "CLS" and "clear" are used and assumed to always be available for both platforms...

# Do any imports for this DEMO as required.
import os
import sys
import random
import time

# Just for this DEMO set all variables as global.
global tlc
global hl
global trc
global vl
global blc
global brc
global fullbox
global shadebox
global topline
global magiceye
global bottomline
global startgap
global count
global grab
global darkcount

# Set the startup variable values.
# tlc == Top lefthand corner character.
# hl == Horizontal line character.
# trc == Top righthand corner character.
# vl == Vertical line character.
# blc == Bottom lefthand corner character.
# brc == Bottom righthand corner character.
# fullbox == Full box character.
# shadebox == Dithered box character.
# count == A re-usable value for this DEMO.
# grab == The psuedo-value to display.
# darkcount == Specific for the shaded "graphics" area only.
tlc=unichr(0x250c)
hl=unichr(0x2500)
trc=unichr(0x2510)
vl=unichr(0x2502)
blc=unichr(0x2514)
brc=unichr(0x2518)
fullbox=unichr(0x2588)
shadebox=unichr(0x2592)
topline=tlc
magiceye="(C)2011, B.Walker, G0LCU."
bottomline=blc
startgap="        "
count=0
grab=255
darkcount=0

# Run continuously until the Ctrl-C keys are pressed.
def main():
	while 1:
		# Set the platform clear screen command for Linux and Windows.
		if sys.platform=="win32": print os.system("CLS"),chr(13),"  ",chr(13),
		if sys.platform=="linux2": print os.system("clear"),chr(13),"  ",chr(13),

		# Randomly generate an 8 bit value as though grabbed from a serial, parallel or USB port.
		grab=int(random.random()*256)
		# Set to a 5 bit value for the DEMO.
		grab=int(grab/8)
		# Although no error should ever occur, never allow one.
		if grab<=0: grab=0
		if grab>=31: grab=31

		# Set up the screen per grab.
		print
		print "A simple pseudo-EM87/6HU6/6E2 tuning indicator style DEMO for standard Python."
		print
		print "Original working idea copyright, (C)2011, B.Walker, G0LCU."
		print
		print "Designed to work on MS Windows, (Vista 32 Bit), using Python 2.6.x."
		print "Also at least Debian Linux using Python 2.6.x too..."
		print
		print
		print "                               EM87/6HU6 simulator."

		# Generate the first line of the MagicEye display.
		topline=startgap+tlc
		count=0
		while count<=61:
			topline=topline+hl
			count=count+1
		topline=topline+trc
		print topline

		# Now generate the MagicEye start only if the grabbed value is GREATER than 0.
		if grab>=1:
			# Do the left hand side very bright part first.
			magiceye=startgap+vl
			count=1
			while count<=grab:
				magiceye=magiceye+fullbox
				count=count+1

			# Now generate the dark centre section.
			count=grab
			darkcount=61-(grab*2)
			while darkcount>=0:
				magiceye=magiceye+shadebox
				darkcount=darkcount-1

			# Finally finish off with another very bright part.
			darkcount=61-(grab*2)
			count=darkcount+grab+1
			while count<=61:
				magiceye=magiceye+fullbox
				count=count+1

		# When the grab value equals 0 override the above and generate a full dark band only.
		if grab==0:
			magiceye=startgap+vl
			count=0
			while count<=61:
				magiceye=magiceye+shadebox
				count=count+1
		# Print the animation to the screen and end with a vertical line.
		print magiceye+vl

		# Now finish off the MagicEye display...
		bottomline=startgap+blc
		count=0
		while count<=61:
			bottomline=bottomline+hl
			count=count+1
		bottomline=bottomline+brc
		print bottomline

		# Finish the screen display.
		print
		print
		print "Grabbed value",grab,"\b..."
		print
		print "Press Ctrl-C to STOP..."
		print

		# Add a short delay for this DEMO...
		time.sleep(0.1)

main()

# End of MagicEye.py DEMO.
# Enjoy finding simple solutions to often very difficult problems. :)

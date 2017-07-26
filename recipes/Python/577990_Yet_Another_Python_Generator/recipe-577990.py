# SweepGen2x.py
#
# A DEMO Audio Sweep Generator from 4KHz down to 100Hz and back up again
# using standard Text Mode Python. Another kids level piece of simple, FREE,
# Test Gear project code...
# This working idea is copyright, (C)2010, B.Walker, G0LCU.
# Written in such a way that anyone can understand how it works.
#
# Tested on PCLinuxOS 2009 and Debian 6.0.0 using Python 2.6.2, 2.6.6 and 2.7.2.
# It may well work on much earlier versions of Python but it is untested...
# "/dev/dsp" IS required for this to work; therefore if you haven't got it then
# install "oss-compat" from you distro's repository. Ensure the sound system is
# not already in use.
# It is easily possible to lengthen the higher frequency playing times and VERY
# easily alter the output level and to speed up or slow down the sweep speed.
# I'll let the big guns do that for you...
# IMPORTANT NOTE:- Every EVEN number of characters is a symmetrical "square" wave
# BUT every ODD number of characters has preference for the "space" by one character.
#
# To run this DEMO type at the Python prompt......
#
# >>> execfile("/full/path/to/SweepGen2x.py")<RETURN/ENTER>
#
# ......and away you go.
#
# Note:- NO import[s] required at all, good eh! ;o)

def main():
	# Set all "variables" as globals, my choice... ;o)
	global mark
	global space
	global freq
	global stringlength
	global n
	global sweep

	# Allocate initial values.
	mark="\xff"
	space="\x00"
	freq=mark+space
	# 8KHz is the default sample speed of the sound system.
	# Therefore this sets the lowest frequency, 8KHz/80=100Hz...
	stringlength=80
	n=0
	sweep=0

	# A simple screen clear and user screen for a default Python window...
	for n in range(0,40,1):
		print "\r\n"
	print "Sweep Generator DEMO from 4KHz down to 100HZ and back again...\n"
	print "This just gives 5 SIREN like sweeps but it is enough for this DEMO...\n"
	print "Copyright, (C)2010, B.Walker, G0LCU.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

	# Open the audio device, "/dev/dsp" for writing.
	audio=open("/dev/dsp", "wb")

	# Sweep for five times only for this DEMO...
	while sweep<=4:

		freq=mark+space
		stringlength=80
		n=0

		while 1:
			# Sweep down from 4KHz to 100Hz.
			# Add a trailing 0x00 character.
			audio.write(freq)
			freq=freq+space
			# Quit when length of "freq" string is 80 characters.
			if len(freq)>=stringlength: break
			audio.write(freq)
			# Add a leading 0xff character.
			freq=mark+freq
			# Quit when length of "freq" string is 80 characters.
			if len(freq)>=stringlength: break
		while 1:
			# Sweep back up again from 100Hz to 4KHz.
			# Start with an empty string.
			freq=""
			# Now create a new square wave string.
			for n in range(0,int((stringlength)/2),1):
				freq=freq+mark
			for n in range(0,int((stringlength)/2),1):
				freq=freq+space
			audio.write(freq)
			# Create a new string reduced by one character.
			# This removes one 0xff character.
			stringlength=stringlength-1
			# Quit when length of "freq" string is 2 characters.
			if len(freq)<=2: break
			# Start with an empty string.
			freq=""
			# Now create a new string reduced by one character.
			for n in range(0,int((stringlength)/2),1):
				freq=freq+mark
			for n in range(0,int(((stringlength)/2)+1),1):
				freq=freq+space
			audio.write(freq)
			# This removes one 0x00 character.
			stringlength=stringlength-1
			# Quit when length of "freq" string is 2 characters.
			if len(freq)<=2: break
		sweep=sweep+1
		# Ensure a complete exit from the loop.
		if sweep>=5: break
	# On exit ensure the audio device is closed.
	audio.close()
main()

# End of SweepGen2x.py DEMO...
# Enjoy finding simple solutions to often VERY difficult problems... ;o)

# Freq_Counter2x.py...
#
# A DEMO audio frequency counter using standard text mode Python.
# (C)2011, B.Walker, G0LCU. Issued as Public Domain.
#
# "/dev/dsp" is required for this to work. If it doesn't exist install
# "oss-compat" from your distro's repository.
# Ensure thet the sound is set up from your distro's audio mixing SW.
#
# Written in such a way that youngsters can understand what is going on.
#
# Tested on PCLinuxOS 2009 and Debian 6.0.0 using Python versions
# 2.5.2, 2.6.6 and 2.7.2. It would probably work down to Python 1.5.2
# but has not been tested to that level.
#
# It will display from <50 Hz to >3500 Hz to withing 0.1% accuracy.
# With a very simple external hardware add-on <30 Hz to >35 KHz is well
# within this DEMOs scope; however for this DEMO only a simple connecting
# cable is needed. Also with a simple code change it is possible to make
# the accuracy to within 0.01% and <5Hz bottom limit.
#
# This is yet another ultra simple piece of audio test gear that can be
# made and understood by a 10 year old...
#
# See my other DEMO uploads of very basic test gear using the sound card
# as the prime mover:-
#
# http://code.activestate.com/recipes/users/4177147/
#
# This is even easier in Python 3.x.x but I'll let the big guns do that for you...
# I HAVE already done it, uploaded it elsewhere and issued it as Public Domain...
#
# This DEMO just requires a virgin text mode Python install and NO imports
# are required either. Banging the metal without special imports or libraries
# and having some functional use too! Good eh!... ;o)
#
# ENJOY...
#
# Bzzza, G0LCU...

def main():
	# Make variables global; my choice... ;o)
	global record
	global n
	global freq
	# Set the startup values...
	freq=0
	record=""
	n=0
	# Connect a 3.2mm jack plug(s) stereo cable from the earphone output
	# to the microphone input; or from a sine/square generator into the
	# microphone input.
	#
	# Using the 1 KHz Audio Function Generator, found here......
	# http://code.activestate.com/recipes/577592-simple-1khz-audio-function-generator-using-standar/?in=user-4177147
	# ......from another Python shell start up this code and generate a sine,
	# square or triangle wave symmetrical waveform.
	#
	# Do NOT exceed 2 Volts peak to peak from an external signal generator!
	#
	# Enter a continuous loop.
	# Grab a file from my Laptop`s, Notebook`s or Netbook`s microphone socket.
	while 1:
		# Do a 1 second recorded burst...
		audio=file('/dev/dsp', 'rb')
		# "record" is the "binary string" to be counted...
		record=audio.read(8000)
		audio.close()
		# Enter another loop to do the count...
		n=0
		freq=0
		while 1:
			# Assume a square wave "mark to space" ratio of 1 to 1 is used,
			# then "wait" until a "space" is found.
			# (For those that don't know.)
			#
			#                  +------+      +---
			# Square wave:-    | Mark |Space |
			#               ---+      +------+
			#
			# This ensures that the loop cycles when NO input is
			# applied to the microphone socket.
			# Exit this loop when "mark" is found or n>=8000...
			while ord(record[n])<=127:
				n=n+1
				# Ensure as soon as n>=8000 occurs it drops out of the loop.
				if n>=8000: break
			# Ensure as soon as n>=8000 occurs it drops completely out of this loop.
			if n>=8000: break
			# Now the "mark" can loop until a "space" is found again and the whole
			# can cycle until n>=8000...
			while ord(record[n])>=128:
				n=n+1
				# Ensure as soon as n>=8000 occurs it drops out of the loop.
				if n>=8000: break
			# Ensure as soon as n>=8000 occurs it drops completely out of this loop.
			if n>=8000: break
			# "freq" will become the frequency of a symmetrical waveform
			# when the above loops are finally exited, n>=8000...
			# Tick up the freq(uency) per "mark to space" cycle.
			freq=freq+1
		# An ultra simple clear screen line...
		# This line is not needed for the demo but added for fullness...
		print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
		# Now display the value in the same place on screen every time.
		# This assumes a 24 or 25 line Python Shell window. Just modify to
		# suit your particular Shell that you use...
		print "\nA simple 50 Hz to 3500 Hz audio frequency counter.\n"
		print "(C)2011, B.Walker, G0LCU. Issued as Public Domain.\n"
		print "Accuracy is within 0.1% of the displayed frequency...\n"
		print "\n\nFrequency is", freq, "Hz...\n\n\n\n\n\n\n\n\n\n\n\n\n"
main()
# End of Freq_Counter.py DEMO.
# Enjoy finding simple solutions to often very difficult problems.

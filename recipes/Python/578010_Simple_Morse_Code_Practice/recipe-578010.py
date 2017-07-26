# MPO2x.py
#
# A DEMO, very crude, Morse Code Practice Oscillator...
# Tested on Debian 6.0.0 using Python 2.6.6 and 2.7.2 and PCLinuxOS 2009 using Python 2.5.2.
# It may well work on earlier Python versions but is untested.
#
# (C)2011-2012, B.Walker, G0LCU. Now issued as Public Domain...
#
# The device, "/dev/audio" is required for this to work. Install "oss-compat" from your
# distro's repository if you haven't got "/dev/audio". Ensure the sound system is NOT
# in use by other programs and use the OS's mixing facilities to set the levels.
#
# Copy the file to the Lib folder(/drawer/directory) or where the modules
# reside as "MPO2x.py"...
#
# For a quick way to run just use at the ">>>" prompt:-
#
# >>> import MPO2x<RETURN/ENTER>
#
# And away we go...
#
# Written in such a way that youngsters can understand what is going on.
#
# Enjoy finding simple solutiuons to often very difficult problems... ;o)

def main():
	# Just three imports required for this DEMO.
	import sys
	import termios
	import tty

	# Set as globals, my choice... ;o)
	global character
	global delay
	global n

	character="(C)2011-2012, B.Walker, G0LCU."
	delay=75
	n=0

	# This is a working function; something akin to the BASIC INKEY$ function...
	# Reference:- http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
	# Many thanks to Danny Yoo for the above code, modified to suit this program...
	# In THIS FUNCTION some special keys do a "break" similar to the "Esc" key inside the program.
	# Be aware of this...
	def inkey():
		fd=sys.stdin.fileno()
		remember_attributes=termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		character=sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
		return character

	while 1:
		# A simple clear screen and user display...
		for n in range(0,32,1):
			print "\n"
		print "A simple crude Morse Code Practice Oscillator...\n"
		print "Press the 'o', 'p' or 'Esc' keys...\n"
		print "Pseudo-paddle simulation, 'o' is the 'dah' and 'p' is the 'dit'...\n"
		print "(C)2011-2012, B.Walker, G0LCU. Issued as Public Domain...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

		# Open "/dev/audio" in write mode...
		audio=open("/dev/audio", "wb")

		# Use the "inkey()" function to get a key character.
		character=inkey()

		# Get out ensuring that the audio device is closed.
		if character==chr(27):
			audio.close()
			break

		# This is a VERY crude simulation of a paddle key to send your Morse Code.
		# It IS quirky, but, is there a better way using standard Text Mode Python?
		# It uses only the keys "o", "O", "p", "P" and "Esc"...
		# Lower case is the slowest speed, upper case the fastest speed.
		delay=0
		if character=="p": delay=75
		if character=="P": delay=50
		if character=="o": delay=225
		if character=="O": delay=150

		# Play a crude sine-wave note at 1KHz of length "delay"...
		for n in range(0,delay,1):
			audio.write(chr(15)+chr(45)+chr(63)+chr(45)+chr(15)+chr(3)+chr(0)+chr(3))
		# Ensure that the audio device is closed after each beep!
		audio.close()
main()

# End of MPO2x.py DEMO...
# Enjoy finding simple solutiuons to often very difficult problems... ;o)

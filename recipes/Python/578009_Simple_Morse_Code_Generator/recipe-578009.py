# MCG2x.py
#
# A simple Morse Code Generator and tutor.
# (C)2010-2012, B.Walker, G0LCU.
#
# A DEMO fun Python program to generate the standard Morse Code tones
# out through the computer's speakers.
#
# Written in such a way that youngsters can understand what is going on.
#
# This is for Python Version 3.x.x using AT LEAST PClinuxOS 2009 and
# Debian 6.0.0...
#
# It is assumed that /dev/audio exists; if NOT, then install oss-compat
# from the distro`s repository.
#
# Ensure the sound system is not already in use.
#
# It is also asumed that the ?nix command "clear" is available.
#
# Copy the file to the Lib folder(/drawer/directory) or where the modules
# reside as "MCG2x.py"...
#
# For a quick way to run just use at the ">>>" prompt:-
#
# >>> import MCG2x<RETURN/ENTER>
#
# And away we go...
#
# Once running just press <ENTER/RETURN> for a random character or INPUT
# any single STANDRAD ASCII character the <RETURN/ENTER> to practice specific
# characters. Type EXIT or QUIT<RETURN/ENTER> to quit...
# Any __unknown__ character will generate the "?" character and display the
# this character along with the Morse Code tones for it...
# Read the Python code below for more information...
#
# Enjoy finding simple solutions to often VERY difficult questions... ;o)

# The standard imports required...
import os
import time
import random
import string

def main():
	# Make variables global, my choice... ;o)
	global delay
	global text
	global ascii_num
	global dah_dit
	global morse_code
	global count

	# Allocate start values...
	delay=225
	text="(C)2010-2012, B.Walker, G0LCU..."
	ascii_num=63
	dah_dit=0
	# The code below is the "?" character for any unknown character entered.
	morse_code="..--.."
	count=0

	while 1:
		# Enter a simple loop...
		# A basic ?nix type screen clear command...
		count=os.system("clear")
		# A simple user screen, QUIT or EXIT<RETURN/ENTER> to STOP...
		print "\nA simple Morse Code Generator and tutor.\n"
		print "(C)2010-2012, B.Walker, G0LCU.\n"
		print "It has a fixed speed of around 8 words per minute...\n"
		text=raw_input("Press <RETURN/ENTER> to continue:- ")
		text=string.upper(text)
		if text=="QUIT" or text=="EXIT": break
		# Don't allow any errors.
		if len(text)>=2: text=""
		if text=="": ascii_num=int(random.random()*43)+48
		if text!="": ascii_num=ord(text)
		# This is the "?" character...
		if ascii_num>=58 and ascii_num<=64:
			morse_code="..--.."
			ascii_num=63
		if ascii_num<=47 or ascii_num>=91:
			morse_code="..--.."
			ascii_num=63
		# Now to generate the relevant code according to the correct ASCII
		# character entered.
		if ascii_num==48: morse_code="-----"
		if ascii_num==49: morse_code=".----"
		if ascii_num==50: morse_code="..---"
		if ascii_num==51: morse_code="...--"
		if ascii_num==52: morse_code="....-"
		if ascii_num==53: morse_code="....."
		if ascii_num==54: morse_code="-...."
		if ascii_num==55: morse_code="--..."
		if ascii_num==56: morse_code="---.."
		if ascii_num==57: morse_code="----."
		if ascii_num==65: morse_code=".-"
		if ascii_num==66: morse_code="-..."
		if ascii_num==67: morse_code="-.-."
		if ascii_num==68: morse_code="-.."
		if ascii_num==69: morse_code="."
		if ascii_num==70: morse_code="..-."
		if ascii_num==71: morse_code="--."
		if ascii_num==72: morse_code="...."
		if ascii_num==73: morse_code=".."
		if ascii_num==74: morse_code=".---"
		if ascii_num==75: morse_code="-.-"
		if ascii_num==76: morse_code=".-.."
		if ascii_num==77: morse_code="--"
		if ascii_num==78: morse_code="-."
		if ascii_num==79: morse_code="---"
		if ascii_num==80: morse_code=".--."
		if ascii_num==81: morse_code="--.-"
		if ascii_num==82: morse_code=".-."
		if ascii_num==83: morse_code="..."
		if ascii_num==84: morse_code="-"
		if ascii_num==85: morse_code="..-"
		if ascii_num==86: morse_code="...-"
		if ascii_num==87: morse_code=".--"
		if ascii_num==88: morse_code="-..-"
		if ascii_num==89: morse_code="-.--"
		if ascii_num==90: morse_code="--.."
		# Now print the result(s)...
		print "\nASCII character "+chr(ascii_num)+"...\n"
		# Note the exclamation marks are NOT an error!
		print "Morse Code!   "+morse_code+"   !\n"
		# Open the "/dev/audio" device for writing...
		audio=open("/dev/audio", "wb")
		for dah_dit in range(0,len(morse_code),1):
			if morse_code[dah_dit]=="-": delay=225
			if morse_code[dah_dit]==".": delay=75
			# Play a crude sine-wave note at 1KHz of length "delay"...
			for count in range(0,delay,1):
				audio.write(chr(15)+chr(45)+chr(63)+chr(45)+chr(15)+chr(3)+chr(0)+chr(3))
			# Add a gap roughly the same as a "dit" and NOT closing the audio device!
			for count in range(0,75,1):
				audio.write(chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0))
		# Ensure that the audio device is closed after each character!
		audio.close()
		# Add a short delay to see the code on screen before starting again.
		time.sleep(1)

main()

# End of MCG2x.py DEMO...
# Enjoy finding simple solutions to often VERY difficult questions... ;o)

# Metronome3x.py
#
# DEMO simple metronome that exploits a minor flaw in the /dev/audio and /dev/dsp devices inside Linux.
# It can tick at around 30 to 400 beats per minute. This minimal code can be improved upon to give
# greater accuracy, range and appearance on screen if required.
#
# Original copyright, (C)2007-2012, B.Walker, G0LCU. Now issued as Public Domain and you may do with
# it as you please.
#
# There is a small flaw that uses the Ctrl-C part of the code. I'll let the big guns tell you users
# that can't find it what it is. It is not a bug as such, but it is a flaw.
#
# Tested on an HP Notebook with Debian 6.0.0 and Python 3.1.3 and an Acer Aspire One Netbook with
# PCLinuxOS 2009 and Python 3.2.1.
# To run just type:-
#
# >>> exec(open("/absolute/path/to/Metronome3x.py").read())<RETURN/ENTER>
#
# And away you go...
#
# $VER: Metronome3x.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.
#
# Enjoy finding simple solutions to often very difficult problems...

# The only import(s) for this DEMO...
import time
import os

def main():
	while 1:
		# the _variable_ listing...
		# "n" is throw away integer number and purposely reused.
		# "beatstring" is the inputted string and is also reused.
		# "beat" is the floating point number from about 0.x to 1.x generated from the inputted data.
		#
		# The standard Linux clear screen cmmand.
		n=os.system("clear")
		# Set up a basic user screen/window.
		print("\nPython 3.x.x simple metronome for the Linux platform.\n")
		print("(C)2007-2012, B.Walker, G0LCU. Issued as Public Domain.\n")
		beatstring=input("Enter any whole number from 30 to 400 (bpm), (QUIT or EXIT to Quit):- ")
		# Allow a means of quitting the DEMO.
		if beatstring=="QUIT" or beatstring=="EXIT": break
		# Don't allow any errors...
		if len(beatstring)>=4: beatstring="100"
		if len(beatstring)<=1: beatstring="100"
		n=0
		while n<=(len(beatstring)-1):
			if beatstring[n]>=chr(48) and beatstring[n]<=chr(57): n=n+1
			else: beatstring="100"
		n=int(beatstring)
		if n<=30: n=30
		if n>=400: n=400
		# Convert this integer "n" back to the "beatstring" string...
		beatstring=str(n)
		# Now convert to the floating point value for the time.sleep() function.
		beat=((60/n)-0.125)
		print("\nApproximate beats per minute = "+beatstring+"...\n")
		print("Press Ctrl-C to enter another speed...")
		while 1:
			# Write directly to the /dev/dsp device.
			try:
				audio=open("/dev/dsp", "wb")
				audio.write(b"\x00\xFF")
				audio.close()
				time.sleep(beat)
			# There is a flaw here, I'll let you big guns find it... ;o)
			# Note it is NOT really a bug!
			except KeyboardInterrupt: break
main()

# End of the Metronome3x.py code.
# Enjoy finding simple solutions to often very difficult problems...

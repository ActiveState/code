# Arduino-Linux2x.py
#
# DEMO Arduino test for STANDARD Python 2.5.x or greater under Linux.
# This is an experimental idea only to test the Arduino Diecimila
# development board under at least STANDARD Python 2.5.x and PCLinuxOS 2009.
#
# This working idea is copyright, (C)2009, B.Walker, G0LCU.
# It is NOW issued entirely as Public Domain, you may do with it as you please.
#
# Copy this 'Arduino-Linux2x.py' file into the drawer of your choice
# and you will be ready to roll... ;-)
# Press ~Ctrl C~ to QUIT, OR, set input to maximum of 5V, i.e. 255. 
#
# To run type:-
# >>> execfile("/full/path/to/Arduino-Linux2x.py")<RETURN/ENTER>
# OR alternatively if it is in the module drawer...
# >>> import Arduino-Linux2x<RETURN/ENTER>
#
# IMPORTANT!!! This DEMO requires root access so take the normal precautions.
# (Now tested on Debian 6.0.0 and Python 2.6.6.)

# Do any imports as required.
import os

# Assume root access!!!
# This is not needed in some cases but added for fullness.
os.system("chmod 666 /dev/ttyUSB0")

# Do a basic clear screen...
os.system("clear")

# NOTE:- The next two system calls are separated for ease of understanding.
# It is assumed that the /dev/ttyUSBx device is /dev/ttyUSB0. If yours is
# not just change the 0 for your number, (0 to 7), below.
# ALSO; pySerial, (and others?), is(/are) NOT needed for this AT ALL.
# Fix the speed of the USB-Serial port to 1200 bps...
os.system("stty -F /dev/ttyUSB0 1200")

# Set it to `raw` transfer mode.
os.system("stty -F /dev/ttyUSB0 raw")

# The program proper.
def main():
	print
	print '      Arduino Diecimila Dev Board access demonsration Python 2.5.x code.'
	print '             Original idea copyright, (C)2008, B.Walker, G0LCU.'
	print '                           Press ~Ctrl C~ to QUIT.'
	print

	while 1:
		# Open up a channel for USB/Serial reading on the Arduino board.
		# Place a wire link between ANALOG IN 0 and Gnd.
		# Replace the wire link between ANALOG IN 0 and 3V3.
		# Replace the wire link between ANALOG IN 0 and 5V.
		# Watch the values change.
		pointer = open('/dev/ttyUSB0', 'rb', 2)

		# Transfer an 8 bit number into `mybyte`.
		mybyte = str(pointer.read(1))

		# Immediately close the channel.
		pointer.close()

		# Print the decimal value on screen.
		print 'Decimal value at Arduino ADC Port0 is:-',ord(mybyte),'.    '

		# Ensure one safe getout when running!
		if mybyte == chr(255): break

main()

# End of program...
# Enjoy finding simple sloutions to often very difficult problems...

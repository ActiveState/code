Python Code:-
=============


# Arduino-WinUAE.py
#
# Arduino test for Python 1.4.x under WinUAE only, NOT classic AMIGAs.
# This is an experimental idea only to test the Arduino Diecimila
# development board under Python 1.4.x and WinUAE.
# (It is assumed that the Python 1.4.x install is in the default drawers.)
# NOTE:- This code also works to Python 2.0.x inside WinUAE.
# This working idea is copyright, (C)2008, B.Walker, G0LCU.
# Copy this 'Arduino-WinUAE.py' file into the 'PYTHON:Lib/' drawer
# and you will be ready to roll... ;-)
# Press ~Ctrl C~ to QUIT, OR, set the input to maximum of 5V, i.e. 255.
#
# It is assumed that you have WinUAE 1.5.3 or greater installed and running a
# minimum of EMULATED classic AMIGA OS 3.0x, 68EC020, 2MB RAM, HDD; that is emulating
# a stock A1200HD and Workbench 3.0x. 
# It is assumed that the SER: device is set up in the AMIGA mode.
# See here for the correct parameters:-
# http://aminet.net/package/dev/src/Arduino_Python
# It is assumed that you know how to allocate the Windows COMx: device to WinUAE.
# It is assumed that you know how to connect and set up the USB Arduino Diecimila
# board inside Windows, (32 bit installs)...
# There may be other forgotten assumptions too, not listed here!
#
# To run type:-
# >>> execfile("PYTHON:Lib/Arduino-WinUAE.py")<RETURN/ENTER>
# NOW issued as Public Domain, you may do with it as you please.
#
# IMPORTANT NOTE:- With a piece of simple home built hardware add-on this WILL work
# on a classic AMIGA A1200 with a standard Serial Port also. For this modification see:-
# http://prdownload.berlios.de/mikeos/ARDUINO.zip

# The program proper.
def main():
	print
	print '      Arduino Diecimila Dev Board access demonsration Python 1.4.x code.'
	print '             Original idea copyright, (C)2008, B.Walker, G0LCU.'
	print '                           Press ~Ctrl C~ to QUIT.'
	print

	while 1:
		# Open up a channel for USB/Serial reading on the Arduino board.
		# Place a wire link between ANALOG IN 0 and Gnd.
		# Replace the wire link between ANALOG IN 0 and 3V3.
		# Replace the wire link between ANALOG IN 0 and 5V.
		# Watch the values change.
		pointer = open('SER:', 'rb', 2)

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
# Enjoy finding simple solutions to often very difficult problems.




Arduino Test.pde code:-
=======================

/* Using the Arduino as a DEMO single channel ADC for Windows XP and Linux. */
/* This idea is copyright, (C)2008, B.Walker, G0LCU. */
/* This is just demonstration code only for use with Python 2.6.x or less. */

/* Set up a variable for basic analogue input. */
int analogue0 = 0;

void setup() {
  /* open the serial port at 1200 bps. This rate is used for purely */
  /* for simplicity only. */
  Serial.begin(1200);

  /* Set the analogue voltage reference, DEFAULT is 5V in this case. */
  analogReference(DEFAULT);
}

void loop() {
  /* Read the 10 bit analogue voltage on analogue input 0. */
  analogue0 = analogRead(0);
  /* Convert to a byte value by dividing by 4. */
  analogue0 = analogue0/4;

  /* Send to the Serial Port the byte value. */
  Serial.print(analogue0, BYTE);
 
  /* Delay 500 milliseconds before taking the next reading. */
  delay(500);
}

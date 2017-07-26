# Campimeter.py
#
# I needed the facility to have a maximised Terminal window on OSX 10.7.5 and this was the result...
# A DEMO to show how to increase the size of a Terminal window and obtain the maximum usable size on a _desktop_.
# The Terminal window must be initially set manually at the uppermost left hand corner and Python started inside
# this window. The colours for this DEMO inside OSX 10.7.5, are grey background, red square and yellow asterisk/characters...
#
# Written in such a way as anyone can understand how it works, youngsters too.
#
# To run type from the Python prompt:-
#
# >>> exec(open("/full/path/to/Campimeter.py).read())<CR>
#
# Where "/full/path/to/" is where you have saved this code; then have a little fun...
#
# This code generates a crude Campimeter... http://en.wikipedia.org/wiki/Campimeter ...and is used to check
# visual field. Just focus on the red square in the centre of the window after pressing <CR> from the initial
# window and then press Ctrl-C immediately after you see an asterisk flash. It is possible to get the Ctrl-C to
# _crash_ out and stop the DEMO if Ctrl-C is pressed at any other time than just after seeing the asterisk flash.
# The cursor has not been turned off and will be seen on the left hand side of the window, so try to ignore it.
#
# $VER: Campimeter.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
# This code is issued as Public Domain and you may do with it as you please.
#
# I have not reset the Terminal back to its original state although all of the information how to do it is in
# this code. Colours are easily reset in Python and I have shown this many times on this site...
#
# Designed and tested on a Macbook Pro, OSX 10.7.5 using Python Versions 2.6.7 and 2.7.1. Also tested on Debian
# Linux 6.0.x using Python versions 2.6.6, 2.7.2 and 3.1.3...
# It would be interesting to see which other platform variants this idea works on; just add a comment...

# All imports required.
import os
import sys
import random
import time

# Ensure Python Version 3.x.x is included...
if sys.version[0]=="3": raw_input=input

# Set some values as global, my choice! ;o)
global row
global column
global attempts

# Allocate initial Terminal window values to be much greater than the allowed Terminal size on the desktop...
row=200
column=300
attempts=0

# Set the Terminal window size larger than its default!
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=row,cols=column))

# Set up a basic user window starting with a grey, cleared window...
print("\033[1;93;100m")
n=os.system("clear")
# Add a delay to allow settings to settle...
time.sleep(1)
print("\n$VER: Campimeter.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("Press the <CR> key to start. After this window is exited focus on")
print("the centred, coloured square. Position yourself until you are both")
print("comfortable and the screen presents a wide field of view. Use the two")
print("keys Ctrl-C if and when you see a randomly positioned _*_ displayed.\n")
print("The larger the display used the better, have fun...\n")
# time.sleep(1)
raw_input("Press the <CR> key to continue...")

# Now get the _new_ real size of the Terminal window...
rows,columns=os.popen("stty size","r").read().split()
row=int(rows)
column=int(columns)

def locate(user_string="$VER: Campimeter.py_Version_0.00.10_(C)2012-2013_B.Walker_G0LCU.",x=0,y=0):
	# Don't allow any user errors. Python's own error detection will check for
	# syntax and concatination, etc, etc, errors.
	x=int(x)
	y=int(y)
	if x>=255: x=255
	if y>=255: y=255
	if x<=0: x=0
	if y<=0: y=0
	HORIZ=str(x)
	VERT=str(y)
	# Plot the user_string at the starting position HORIZ, VERT...
	print("\033["+VERT+";"+HORIZ+"f"+user_string)

def main():
	# Ensure certain _variables_ remain global, my choice... ;o)
	global row
	global column
	global attempts

	# Note:- row and colour are already set.
	attempts=0

	# Clear the window for the test.
	n=os.system("clear")

	# Set the centred red square for the start...
	locate("\033[0;41;41m  \033[1;93;100m ",int(column/2),int(row/2))

	# This is set for 5 possible attempts only. Just change the number 5 to your number of attempts.
	for n in range(0,5,1):
		try:
			# Have a random start waiting time...
			waiting_time=int(random.random()*6)
			time.sleep(waiting_time)
			coloured_spot_column=int(random.random()*int(columns))
			coloured_spot_row=int(random.random()*int(rows))
			# Display a coloured asterisk randomly on screen for a brief period...
			locate("\033[1;93;100m*\033[1;93;100m ",coloured_spot_column,coloured_spot_row)
			# This is the timer to display the asterisk and is made relatively easy...
			time.sleep(0.2)
			# Clear this displayed asterisk...
			locate("\033[1;93;100m \033[1;93;100m ",coloured_spot_column,coloured_spot_row)
			# Because this code does not detect whether the red square might be overwritten,
			# ensure that it is redrawn at the centre of the Terminal window.
			locate("\033[0;41;41m  \033[1;93;100m ",int(column/2),int(row/2))
			# Hold long enough to react to Ctrl-C...
			time.sleep(1)
		except KeyboardInterrupt:
			# After pressing Ctrl-C ensure ^c or ^C is not seen on the screen and update.
			print("\b\b\b\b    ")
			attempts=attempts+1
			time.sleep(1)

	# Give the results for this fun project and re-run if required...
	print("You had "+str(attempts)+" successes out of "+str((n+1))+" possible attempts...\n")
	again=raw_input("Do you want to try again? (Y/N):- ")
	if again=="y" or again=="Y": main()

main()
# It is easy to reset the Terminal back to the default sze AND colours using the methods already shown.
# I have not bothered, as the intent of this DEMO is to show how to increase the size of the Terminal
# window and obtain the real, new size too.

# End of Campimeter.py DEMO.
# Enjoy finding simple solutuions to often very difficult problems...

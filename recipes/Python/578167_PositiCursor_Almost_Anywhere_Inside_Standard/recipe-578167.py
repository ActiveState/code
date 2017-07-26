# Locate_Demo.py
#
# A DEMO showing the power of the ANSI (ASCII) _Esc_ codes in standard text mode Python.
# This test code was originally written in 2007 for Python 1.4.0 on a standard AMIGA A1200(HD).
# It is now brought up to date and ALSO works on Linux up to Python 3.2.2...
# This code works on Classic AMIGAs, WinUAE and E-UAE using AmigaOS 3.1x and Python
# Version(s) 1.4.0 to 2.0.1, PcLinuxOS 2009 using Python 2.5.2, 2.6.1 and 3.2.2 and
# Debian Linux using Python 2.6.6, 2.7.2 and 3.1.3.
#
# ANSI _Esc_ codes here:-    http://www.termsys.demon.co.uk/vtansi.htm
#
# Issued as Public Domain, you may do with it as you please.
#
# It draws a text mode triangle inside a Python Terminal, writes a string inside that triangle,
# writes a string BELOW the triangle and then resets the cursor to the top of the screen awaiting
# user input. After pressing the <CR> key the screen is cleared and a new text mode _sine_wave_
# graph is plotted, again awaiting user input to clear the screen, finally placing the cursor at
# the top of the Terminal window along with the default string being printed...
# It uses a simple function to draw an ASCII character or string on screen starting at a given,
# [column, line], location.
#
# This function is as thus:-
#
# >>> locate(user_string, horizontal_position, vertical_position)<CR>
#
# <user_string> is a string type, and, <horizontal_position> and <vertical_position> are inetger
# types from 0, (zero) to 255...
#
# The easiest way to run this code, (depending upon the platform), is to type......
#
# >>> exec(open("/full/path/to/Locate_Demo.py").read())<CR>
#
# ......and away you go.
#
# $VER: Locate_Demo.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.

# The only imports required for this demo...
import math
import sys

# Make the whole code 3.x.x compatible too...
if sys.version[0]=="3": raw_input=input

# The only _varaibles_ required for this DEMO...
char="*"
x=20
y=19

# A Simple clear screen command for this DEMO...
for n in range(0, 64, 1): print("\r\n")

# This function is just basic for this DEMO but shows the power of the ANSI _Esc_ codes...
def locate(user_string="$VER: Locate_Demo.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.", x=0, y=0):
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
	# Plot the user_string at the starting at position HORIZ, VERT...
	print("\033["+VERT+";"+HORIZ+"f"+user_string)

# Plot the upwards slope of the triangle...
while x<=35:
	locate(char, x, y)
	x=x+1
	y=y-1

# Plot the downwards slope of the triangle...
while x<=52:
	locate(char, x, y)
	x=x+1
	y=y+1

# Plot the base of the triangle...
char="***********************************"
locate(char, 19, 20)

# Write a string inside the triangle...
char="Drawing in text mode Python."
locate(char, 23, 18)

# Print this line BELOW the triangle...
print("\n\n\nCursor now set to the top.")
# NOW reset the cursor back to the top of the window using the default x and y values.
locate("")

# Hold drawing until user input for sine wave plot...
char=raw_input("Press <CR> to continue with a _sine_ wave:- ")

# A Simple clear screen command for this DEMO...
for n in range(0, 64, 1): print("\r\n")

char="*"
x=3
y=12

# Now plot a sinewave curve inside the Terminal.
for angle in range(0, 360, 5):
	# Generate a FLOATING point sine(angle) value...
	angle=float(angle)
	y=math.sin((angle*(math.pi))/180.0)
	# INVERT, AND, keep the y scan inside the standard Terminal window size.
	y=12-(int(y*10))
	locate(char, x, y)
	# Move along one, (1), x position.
	x=x+1

# Hold drawing until user input for a final clear screen...
char=raw_input("\n\n\n\n\n\n\n\n\n\nPress <CR> to clear the screen, display the default string, and stop:- ")

# A Simple clear screen command for this DEMO...
for n in range(0, 64, 1): print("\r\n")

# NOW reset the cursor back to the top of the window using the default x and y values
# and display the locate() function's default string...
locate()

# End of Locate_Demo.py Python code...
# Enjoy finding simple solutions to often very difficult problems...

# Colour_Bar.py
#
# Linux, (UNIX?), only. Issued as Public Domain and you may do with this as you please...
#
# This is a useful bit of simple code to generate, (in a default, 80 x 24 text window), half
# of the window with a colourbar and the other half with a greyscale. A simple piece of
# testgear of yesteryear that would be of full use inside a Console as opposed to a Terminal...
#
# To hide the cursor it assumes the "tput" command is available...
# If not then try "setterm -cursor off" in its place, see below...
#
# IMPORTANT NOTE:- The Esc sequence colours generated do NOT conform entirely to ISO 6429 standards.
# On exiting the whole window is reset back to its orginal state and cleared with a simple
# (C) line and another line printed as proof...
# A bonus section is added printing the ANSI and (NON) ISO colours, IF, available. Just scroll up and
# down to see these colours and attributes and then press Ctrl-C to finally quit.
#
# To run, type from the any version of the Python prompt......
#
# >>> exec(open("/full/path/to/Colour_Bar.py").read())<CR>
#
# ......and away you go! ;o)
#
# Tested on default Terminals in PCLinuxOS 2009 using Python 2.5.2 and 3.2.2, Debian 6.0.0 using
# Python 2.6.6, 2.7.1 and 3.1.3 and Mac OSX 10.7.5 using Python 2.5.6, 2.6.7 and 2.7.1...
#
# $VER: Colour_Bar.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Written in such a way so that anyone can see and understand how it works...
#
# Enjoy finding simple solutions to often very difficult problems...

# Ensure this works on _any_ Version of Python...
import os
import sys
if sys.version[0]=="3": raw_input=input

# Do a simple clear screen, and ensure white on black.
for n in range(0,32,1): print("\033[0;37;40m                                                                                ")
print("\033[0;0f")

print("$VER: Colour_Bar.py_Version_0.00.10_Public_Domain_2012_B.Walker_G0LCU.\n")
print("A colour bar and greyscale generator for standard text mode Python.\n")

raw_input("Press <CR> to display and <CR> again to continue:- ")

# Print 12 lines of colour bars...
for n in range(0,12,1):
	print("\033[0;97;107m          \033[0;93;103m          \033[0;36;46m          \033[0;32;42m          \033[0;35;45m          \033[0;31;41m          \033[0;44;44m          \033[0m")
# Print 11 lines of grey scales...
for n in range(0,11,1):
	print("\033[0;30;40m                    \033[0;90;100m                    \033[0;37;47m                    \033[0;97;107m                    ")
# The last grey scale line pseudo-hiding the cursor by shifting it to the light grey section...
print("\033[0;30;40m                    \033[0;90;100m                    \033[0;37;47m                    \033[0;0f")

# Hide and restore the cursor as required.
n=os.system("tput civis")
raw_input("\033[0;0f\033[0;90;100m")
n=os.system("tput cnorm")

# Do a simple clear screen again...
# ...and reset the cursor towards the top left hand corner...
for n in range(0,32,1): print("\033[0m                                                                                ")
print("\033[0;0f")

print("$VER: Colour_Bar.py_Version_0.00.10_Public_Domain_2012_B.Walker_G0LCU.\n")
print("Finally a colour listing for your reference for your Terminal emulator.\n")
print("Just scroll up and down to view...\n")
raw_input("Press <CR> to continue:- ")

print("\nANSI standard...")
print("Various _font_ modes and et cetera...")
for d in range(0,10,1): print("\\033["+str(d)+"m = \033[%dmColour display...\033[0m" % d)

print("\nANSI AND ISO 6429 standard colours...")
print("Foreground colours...")
for d in range(30,38,1): print("\\033["+str(d)+"m = \033[%dmColour display...\033[0m" % d)
print("\nBackground colours...")
for d in range(40,48,1): print("\\033["+str(d)+"m = \033[%dmColour display...\033[0m" % d)

print("\nNON-ANSI and NON-ISO 6429 standard colours...")
print("High intensity foreground colours...")
for d in range(90,98,1): print("\\033["+str(d)+"m = \033[%dmColour display...\033[0m" % d)
print("\nHigh intensity background colours...")
for d in range(100,108,1): print("\\033["+str(d)+"m = \033[%dmColour display...\033[0m" % d)

print("\nPress Ctrl-C to quit...")

while 1: pass

# Colours.py
#
# This DEMO script prints colours and codes for Linux, Classic AMIGA and Windows Python.
#
# This is Public Domain and you may do with it as you please.
#
# Tested on standard classic AMIGA A1200(HD), E-UAE, Debian Linux, Windows XP and Vista,
# and WinUAE from Python 1.4.0 to 3.3A2.
#
# This shows how to enhance text printouts to the screen for better presentation.
# Windows is limited to a complete switch of the whole window to only foreground
# and background. The AMIGA and derivatives are limited to ONLY the first eight
# WorkBench colours. Linux is unable to do ITALICS reliably on various terminal
# programs using the escape mode method...
#
# Because of a fun program I uploaded that was voted down I decided to upload this
# because although some may know about it, MANY won't! I will say no more about the fun
# program. This does NOT do anything to your personal Terminal setups except display
# various modes and colours at the flick of a simple escape sequence.
#
# Copy/drag this file to the Lib(rary) directory/folder/drawer, rename to Colours.py
# and run from the Python Prompt using:-
#
# >>> import Colours<RETURN/ENTER>
#
# And away you go...
#
# $VER: Colours.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Enjoy finding simple solutions to often very difficult problems...

# The only, (standard), imports required for this DEMO...
import sys
import os
import time

print("\nColours inside a Linux Terminal, Classic AMIGA CLI")
print("or Windows Command Prompt using Python.")

# The code is self explanatory...
if sys.platform=="linux2" or sys.platform=="darwin":
	print("\n\033[0mThis line is your startup defaults...")
	print("\n      \033[0;37;40mNormal Colors.\033[0m       \033[1;37;40mBright, Bold, Foregrond Colors.\033[0m\n")
	print("  \033[0;30;47m Black      \033[0m 0;30;47m      \033[1;30;40m Dark Gray      \033[0m 1;30;40m")
	print("  \033[0;31;47m Red        \033[0m 0;31;47m      \033[1;31;40m Bright Red     \033[0m 1;31;40m")
	print("  \033[0;32;47m Green      \033[0m 0;32;47m      \033[1;32;40m Bright Green   \033[0m 1;32;40m")
	print("  \033[0;33;47m Brown      \033[0m 0;33;47m      \033[1;33;40m Yellow         \033[0m 1;33;40m")
	print("  \033[0;34;47m Blue       \033[0m 0;34;47m      \033[1;34;40m Bright Blue    \033[0m 1;34;40m")
	print("  \033[0;35;47m Magenta    \033[0m 0;35;47m      \033[1;35;40m Bright Magenta \033[0m 1;35;40m")
	print("  \033[0;36;47m Cyan       \033[0m 0;36;47m      \033[1;36;40m Bright Cyan    \033[0m 1;36;40m")
	print("  \033[0;37;40m Light Grey \033[0m 0;37;40m      \033[1;37;40m White          \033[0m 1;37;40m")
	print("\n\033[0;4;37;40mUnderlined text...\033[0m")
	print("\n\033[1;4;37;40mBright, bold, underlined text...\033[0m")
	print("\n\033[0mFinally reset the colours back to your startup defaults...\nPress Ctrl-C to Quit:- ")

if sys.platform=="amiga":
	print("\n\033[0mThis line is your startup defaults...")
	print("\n\033[0mThe first eight WorkBench colours only! (Assume default bootup colours.)\n")
	print("  \033[0;30;41m White on black 0;30;41m, \033[0;32;41mbright white on black, 0;32;41m... \033[0m")
	print("  \033[1;30;43m Bold white on user background, 1;30;43m... \033[0m")
	print("  \033[0;3;32;44m Normal, italic, bright, white on user background, 0;3;32;44m... \033[0m")
	print("  \033[1;3;32;45m Bold, italic, bright, white on user background, 1;3;32;45m... \033[0m")
	print("  \033[0;4;31;46m Normal, underlined, black on user background, 0;4;31;46m... \033[0m")
	print("  \033[1;3;4;31;47m Bold, italics, underlined, black on user background, 1;3;4;31;47m... \033[0m")
	print("\n\033[0mFinally reset the colours back to your startup defaults...\nPress Ctrl-C to Quit:- ")

if sys.platform=="win32":
	# Normal colours for a Command Prompt from CMD.EXE is white on black.
	os.system("COLOR 07")
	print("\nNormal Command Prompt default colours, white on black...\n")
	# Hold for about 2 seconds...
	time.sleep(2)
	# This sets the whole page to green on black.
	os.system("COLOR 0A")
	print("Refer to the COLOR command for choice of colours.\nThis is green on black for about four seconds...\n")
	# Hold for about 4 seconds before bringing back to standard colours...
	time.sleep(4)
	# These are the default foreground and background colours.
	os.system("COLOR 07")
	print("Back to the default foreground and background colours...\nPress Ctrl-C to Quit:- ")	

while 1: pass
# End of Colours.py code.
# Enjoy finding simple solutions to often very difficult problems...

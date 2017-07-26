# hexdump.py
#
# Original idea, (C)2006-2016, B.Walker, G0LCU.
# Issued as Creative Commons CC0 licence.
# Modified to suit _all_ versions of python.
#
# exec(open("Full path to hexdump.py").read())
# For all versions OR...
# execfile("Full path to hexdump.py")
# ...for versions 2.x.x and below.
# Works from Python 1.4.0 to 3.5.2 without modification.
#
# IMPORTANT! There is NO error checking in this code. It relies entirely
# on Python's own tracebacks for user and/or programming errors.
#
# Tested on:-
# 1) Classic stock AMIGA A1200(HD), OS 3.0x, with Python, 1.4.0 to 2.0.1.
#    WinUAE and FS-UAE running AMIGA OS 3.1x. (E-UAE might work too.)
# 2) Windows 8.1, with Python, 2.7.9 and 3.4.3.
# 3) OSX 10.7.5, OSX 10.11.6, with Python 2.5.x, 2.6.x, 2.7.x and 3.5.2.
# 4) Ubuntu 16.04, 64 bit, with Python 2.7.11 and 3.5.1.
#
# Obviously there are versions missed out as I no longer have them,
# but suffice it to say that this was written around an AMIGA about 10 years
# ago so I decided to make it universal recently and issue as a fun project...

import sys
if sys.version[0]>="3": raw_input=input

filename=raw_input("Full path and filename, then press ENTER:- ")
binary=open(filename,"rb+")
length=len(binary.read())
array=""
for position in range(0,length,1):
	binary.seek(position)
	char=hex(ord(binary.read(1)))[2:]
	if len(char)<=1: char="0"+char
	# Remove the whitespace for a pure hex-string.
	# array=array+char
	array=array+char+" "
binary.close()

# Create a pseudo-array, whitespace delimited, this line can be ommitted.
# Bending the rules of print as a statement and as a function here. ;o)
print("%s" %(array))

# Save the text _hex_ dump as the original filename with the '.hex' extension.
# In this specification the HEX file length should be exactly 3 times the size
# of the original binary file length. It is deliberately whitespace delimited.
filename=filename+".hex"
hexadecimal=open(filename,"w")
hexadecimal.write(array)
hexadecimal.close()

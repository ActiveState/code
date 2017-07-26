# Forwards_Compatibility.py
#
# A DEMO generating a function on the fly...
#
# A DEMO showing how to use "bytes" and "string" classes/types inside the same code to access
# _directly_, say, the sound devices in Linux. The code as it stands runs on the paltforms
# and versions shown below...
#
# Many thanks to Daniel Lepage who showed me the way to change strings to bytes the Python way.
# This opened the door that I was looking for to write to the /dev/dsp device in Linux universally.
# It is NOT possible to use the bytes class and string class in one common Python code, (accessing
# a HW device in Linux), from Python 1.4.0 to 3.3A2, until now.
#
# When this code is run in versions Python 2.7.x down to 1.4.0, (inside Windows Vista 32 bit,
# PCLinuxOS 2009, Debian 6.0.0, Classic AMIGA A1200(HD), WinUAE and E-UAE), the "if" statement
# is completely ignored and the string is just a plain string class/type. HOWEVER when Python
# Versions 3.x.x is encountered the "if" statement comes into play. The "def_string" is a Python
# function in its own right and when executed using the "exec" statement becomes that fuction
# in reality; in ths case as "t2b(some_string)"; t2b(some_string) is then called to convert the
# "byte_string" into a bytes class/type.
#
# If the hashes are removed accessing the audio in Linux then this is a real case scenario for
# its usage. I can now progress using the /dev/dsp universally instead of having two lots of code
# doing the same thing...
#
# $VER: Forwards_Compatibility.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Issued under the MIT licence...
#
# =============================================================================
# Python 3.1.3 (r313:86834, Nov 28 2010, 10:01:07) 
# [GCC 4.4.5] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> exec(open('/home/wisecracker/Desktop/Code/Forwards_Compatibility.py').read())
# b'\x00\x00\x00\x00\xff\xff\xff\xff'
# 8
# <class 'bytes'>
# >>> dir()
# ['__builtins__', '__doc__', '__name__', '__package__', 'byte_string', 'def_string', 'sys', 't2b']
# >>> print(def_string)
# def t2b(some_string):
#	decimals=[ord(char) for char in some_string]
#	return bytes(decimals)
#
# >>> _
# =============================================================================
# Python 2.6.6 (r266:84292, Dec 26 2010, 22:31:48) 
# [GCC 4.4.5] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> execfile('/home/wisecracker/Desktop/Code/Forwards_Compatibility.py')
# ????
# 8
# <type 'str'>
# >>> dir()
# ['__builtins__', '__doc__', '__name__', '__package__', 'byte_string', 'sys']
# >>> print(def_string)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'def_string' is not defined
# >>> _
# =============================================================================
# Both as predicted...
#
# Finally the Python Versions tested on:-
# AMIGA variants:- 1.4.0, 2.0.1.
# Windows Vista 32 bit:- 2.0.1, 2.1.3, 2.2.3, 2.3.2, 2.4.4, 2.5.4, 2.6.6, 2.7.2,
# 3.0.1, 3.2.1, 3.3A2.
# PCLinuxOS 2009 and Debian 6.0.0:- 2.4.6, 2.5.2, 2.6.2, 2.6.6, 2.7.2, 3.1.3, 3.2.2.

# An important import...
import sys

# Ensure global for all Python versions and platforms under test...
global byte_string

# A simple _square_wave_ string for Linux audio systems...
byte_string=chr(0)+chr(0)+chr(0)+chr(0)+chr(255)+chr(255)+chr(255)+chr(255)

# Ensure forwards compatibility...
if sys.version[0]=="3":
	# The string below is in reality a slightly more friendly version of this function from Daniel Lepage:-
	# def t2b(some_string):
	#	decimals = [ord(c) for c in some_string]
	#	return bytes(decimals)
	def_string="def t2b(some_string):\n\tdecimals=[ord(char) for char in some_string]\n\treturn bytes(decimals)\n"
	# Execute the string to generate the function on the fly...
	exec(def_string)
	# Now call the newly generated function...
	byte_string=t2b(byte_string)

# See above for a printout...
print(byte_string)
# This line should read 8 only.
print(len(byte_string))
# This line should print the string or bytes class/type depending on the runtime.
print(type(byte_string))

# Thses lines are for a physical test inside Linux flavours with /dev/dsp available...
#
# audio=open("/dev/dsp", "wb")
# for n in range(0, 1000, 1):
#	audio.write(byte_string)
# audio.close()
#
# Just remove the hashes for the four lines to have a real world test in Linux...

# End of Forwards_Compatibility.py DEMO...
# Enjoy finding simple solutions to often very difficult problems...

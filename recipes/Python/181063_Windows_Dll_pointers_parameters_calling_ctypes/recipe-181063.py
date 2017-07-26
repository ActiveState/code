# PROGRAM NAME : HLLAPI interface - ctypes version
# Author: Stefano Spinucci
# Written: 2002/02/16
# DESCRIPTION
# This program interface the 3270 HLLAPI library of an Italian 3270 emulator using 
# the ctypes library (home page : http://starship.python.net/crew/theller/ctypes.html
# or on sourceforge : http://sourceforge.net/projects/ctypes)
# The calling scheme for the function is :
# void FAR PASCAL hllapi(int FAR *, char FAR *, int FAR *, int FAR *);
# NOTE : 
# <from ctypes docs> Internally ctypes makes heavy use of the new type system introduced 
# in Python 2.2, so it will not work in earlier versions.

from ctypes import windll, c_int, c_string, c_char_p, byref

# ------------------------------------------------------------------------------------------------
# dll initialization
# ------------------------------------------------------------------------------------------------
#Load the dll 'Ehllapi.dll' (the file .py is in the same directory of the dll)
Ehllap32 = windll.ehllap32
#Load the function 'hllapi' from the dll
hllapi = Ehllap32.hllapi

# ------------------------------------------------------------------------------------------------
# variables setting and function calling
# ------------------------------------------------------------------------------------------------
#Set the variables
h_func = c_int(1)
h_text = c_string('A')
#alternatively to "h_text = c_string('A')" you can use "h_text = c_char_p('A')"
h_len = c_int(1)
h_ret = c_int(999)

#Function calling
hllapi(byref(h_func), h_text, byref(h_len), byref(h_ret))

#Print the value returned
print h_func.value
print h_text.value
print h_len.value
print h_ret.value






# PROGRAM NAME : HLLAPI interface - calldll version
# Author: Stefano Spinucci
# Written: 2002/02/16
# DESCRIPTION
# This program interface the 3270 HLLAPI library of an Italian 3270 emulator using 
# the calldll library (from Sam Rushing http://www.nightmare.com/software.html)
# I've found very useful also edll.py from http://pages.ccapcable.com/lac/undergroundPython.html
# The calling scheme for the function is :
# void FAR PASCAL hllapi(int FAR *, char FAR *, int FAR *, int FAR *);

# ------------------------------------------------------------------------------------------------
# Function defining : 
# - myPrintLong : given a membuf with a long inside, print the long
# - myPrintString : given a membuf with a string inside, print the string
# - mySetLong : given a membuf with len = 4, set his value with the long passed
# - mySetString : given a membuf, set his value with the string passed (adding the character \0)
# ------------------------------------------------------------------------------------------------

def myPrintLong(vVar):
	#Print the long (first way)
	a= struct.unpack('I', vVar.read())[0]
	print a

	#Print the long (second way)
	print calldll.read_long(vVar.address())

def myPrintString(vVar):
	#Print the string (first way)
	a = vVar.read()
	print a[:len(a)-1]
	print len(a)

	#Print the string (second way)
	a = calldll.read_string(vVar.address())
	print a
	print len(a)

def mySetLong(vMemBuf, vValueToSet):
	string_packed = struct.pack("L",vValueToSet) # packed as unsigned long
	vMemBuf.write(string_packed)

def mySetString(vMemBuf, vValueToSet):
	data_len = len(vValueToSet) 
	pack_format = str(data_len+1)+"s" # add one for \0 at the end. 
	string_packed = struct.pack(pack_format, vValueToSet) # pack() will add \0 for us
	vMemBuf.write(string_packed)

# ------------------------------------------------------------------------------------------------
# Import the required library
# ------------------------------------------------------------------------------------------------

#Import the calldll module
import calldll
#Import the struct module (a standard python module)
import struct

# ------------------------------------------------------------------------------------------------
# Get the handle of the dll and the address of the function
# ------------------------------------------------------------------------------------------------

#Get the handle of the Dll
handle = calldll.load_library ('C:\Tee3270\Ehllap32')

#Get the address of the function
address = calldll.get_proc_address (handle, 'HLLAPI')

# ------------------------------------------------------------------------------------------------
# Initialization
# ------------------------------------------------------------------------------------------------
# vFunction, vTextLen and vResult are defined as a membuf with lenght = 4, because 4 is the lenght 
# of an unsigned long packed with struct.pack("L", NumberToPack)
vFunction = calldll.membuf(4)
vTextLen = calldll.membuf(4)
vResult = calldll.membuf(4)
# vFunction is defined as a membuf with lenght = 1921 because the dll needs a buffer of 
# 1920 char + 1 for \0 at the end
# You can here define a membuf of the lenght you need + 1 for the last \0 character
vText = calldll.membuf(1921)

# ------------------------------------------------------------------------------------------------
# Function calling
# ------------------------------------------------------------------------------------------------

# Vars setting
#1
mySetLong(vFunction, 1)
#2
string_value_to_write = 'A'
mySetString(vText, string_value_to_write)
#3
mySetLong(vTextLen, len(string_value_to_write))
#4
mySetLong(vResult, 1)

#Call the function
calldll.call_foreign_function (
			address,
			'llll',
			'l',
			(vFunction.address(), vText.address(), vTextLen.address(), vResult.address())
			)


myPrintLong(vResult)
myPrintString(vText)

# ------------------------------------------------------------------------------------------------
# Dll unloading
# ------------------------------------------------------------------------------------------------

#Unload the dll
calldll.free_library (handle)

# d2b.py
#
# Decimal to byte(s) and character/string to byte(s) converter.
# Any decimal number from 0 to 255 converted to b"\x??" format.
# Any standard ASCII string, something like "\x00Some String.\xFF" converted
# to b"\x00Some String.\xff". NOTE:- "FF" is displayed as "ff" on conversion
# but the end result is the same.
#
# NOTE:- The reverse, b"\x00Some String.\xff" converted to
# "\x00Some String.\xff", is easy and therefore not included in this function.
#
# What I needed......
# The function, sometext=chr(a+b), (where "a" could be for example 127 and
# "b" in this case is -127<=b<=128), capability is not easily possible with the
# b"string" byte(s) format so this function was devised.
#
# See here for an example of chr(a+b):-
# http://code.activestate.com/recipes/578013-amplitude-modulation-tremolo-was-an-audiosound-sni/?in=lang-python
#
# This new function uses NO import(s), nor any special programming style,
# but is written so that anyone can understand, (including kids), how it works.
# It does NOT need any special encoding or any other "Pythonic" requirements at all.
# It is not "elegant", as professionals may call it, but, it is functional.
#
# I have no idea at all as to the upper limit of ASCII string length it can
# handle, however it CAN handle a(n) "", (empty), string.
#
# ==========================================================================
#
# Python 3.1.3 (r313:86834, Nov 28 2010, 10:01:07) 
# [GCC 4.4.5] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> exec(open('/home/G0LCU/Desktop/Code/d2b.py').read())
# >>> a=78
# >>> type(a)
# <class 'int'>
# >>> b=d2b(a)
# >>> print(b)
# b'N'
# >>> type(b)
# <class 'bytes'>
# >>> text="\x00(C)2012, B.Walker, G0LCU.\xFF"
# >>> len(text)
# 27
# >>> type(text)
# <class 'str'>
# >>> newtext=t2b(text)
# >>> len(newtext)
# 27
# >>> print(newtext)
# b'\x00(C)2012, B.Walker, G0LCU.\xff'
# >>> type(newtext)
# <class 'bytes'>
#
# ============================================================================
#
# Copyright, (C)2012, B.Walker, G0LCU.
# Issued under GPL2 licence...
# Enjoy finding simple solutions to often very difficult problems.
#
# Requires Python Version 3.x.x only.
# Tested on Debian 6.0.0 using Python 3.1.3, and PCLinuxOS 2009 using Python 3.2.1.
# Also Tested on MS Windows Vista, 32 bit, using Python 3.0.1 and Python 3.2.2.

# Decimal number to byte(s) string converter.
def d2b(a,b=0):
	# "a" any decimal number between 0 to 255.
	# "b" is reserved, but for my usage is very useful, see above... ;o)
	# Don't allow any floating point numbers.
	a=int(a)
	b=int(b)
	decimal=a+b
	# Out of range checks forcing function to exit!
	if decimal<=-1 or decimal>=256:
		print("\nError in d2b(a,b=0) function, decimal integer out of range, (0 to 255)!\n")
		# FORCE a Python error to stop the function from proceeding; "FORCED_HALT" IS NOT DEFINED!
		print(FORCED_HALT)
	# Convert new decimal value 0 to 255 to b"\x??" value.
	if decimal==0: newbyte=b"\x00"
	if decimal==1: newbyte=b"\x01"
	if decimal==2: newbyte=b"\x02"
	if decimal==3: newbyte=b"\x03"
	if decimal==4: newbyte=b"\x04"
	if decimal==5: newbyte=b"\x05"
	if decimal==6: newbyte=b"\x06"
	if decimal==7: newbyte=b"\x07"
	if decimal==8: newbyte=b"\x08"
	if decimal==9: newbyte=b"\x09"
	if decimal==10: newbyte=b"\x0A"
	if decimal==11: newbyte=b"\x0B"
	if decimal==12: newbyte=b"\x0C"
	if decimal==13: newbyte=b"\x0D"
	if decimal==14: newbyte=b"\x0E"
	if decimal==15: newbyte=b"\x0F"
	if decimal==16: newbyte=b"\x10"
	if decimal==17: newbyte=b"\x11"
	if decimal==18: newbyte=b"\x12"
	if decimal==19: newbyte=b"\x13"
	if decimal==20: newbyte=b"\x14"
	if decimal==21: newbyte=b"\x15"
	if decimal==22: newbyte=b"\x16"
	if decimal==23: newbyte=b"\x17"
	if decimal==24: newbyte=b"\x18"
	if decimal==25: newbyte=b"\x19"
	if decimal==26: newbyte=b"\x1A"
	if decimal==27: newbyte=b"\x1B"
	if decimal==28: newbyte=b"\x1C"
	if decimal==29: newbyte=b"\x1D"
	if decimal==30: newbyte=b"\x1E"
	if decimal==31: newbyte=b"\x1F"
	if decimal==32: newbyte=b"\x20"
	if decimal==33: newbyte=b"\x21"
	if decimal==34: newbyte=b"\x22"
	if decimal==35: newbyte=b"\x23"
	if decimal==36: newbyte=b"\x24"
	if decimal==37: newbyte=b"\x25"
	if decimal==38: newbyte=b"\x26"
	if decimal==39: newbyte=b"\x27"
	if decimal==40: newbyte=b"\x28"
	if decimal==41: newbyte=b"\x29"
	if decimal==42: newbyte=b"\x2A"
	if decimal==43: newbyte=b"\x2B"
	if decimal==44: newbyte=b"\x2C"
	if decimal==45: newbyte=b"\x2D"
	if decimal==46: newbyte=b"\x2E"
	if decimal==47: newbyte=b"\x2F"
	if decimal==48: newbyte=b"\x30"
	if decimal==49: newbyte=b"\x31"
	if decimal==50: newbyte=b"\x32"
	if decimal==51: newbyte=b"\x33"
	if decimal==52: newbyte=b"\x34"
	if decimal==53: newbyte=b"\x35"
	if decimal==54: newbyte=b"\x36"
	if decimal==55: newbyte=b"\x37"
	if decimal==56: newbyte=b"\x38"
	if decimal==57: newbyte=b"\x39"
	if decimal==58: newbyte=b"\x3A"
	if decimal==59: newbyte=b"\x3B"
	if decimal==60: newbyte=b"\x3C"
	if decimal==61: newbyte=b"\x3D"
	if decimal==62: newbyte=b"\x3E"
	if decimal==63: newbyte=b"\x3F"
	if decimal==64: newbyte=b"\x40"
	if decimal==65: newbyte=b"\x41"
	if decimal==66: newbyte=b"\x42"
	if decimal==67: newbyte=b"\x43"
	if decimal==68: newbyte=b"\x44"
	if decimal==69: newbyte=b"\x45"
	if decimal==70: newbyte=b"\x46"
	if decimal==71: newbyte=b"\x47"
	if decimal==72: newbyte=b"\x48"
	if decimal==73: newbyte=b"\x49"
	if decimal==74: newbyte=b"\x4A"
	if decimal==75: newbyte=b"\x4B"
	if decimal==76: newbyte=b"\x4C"
	if decimal==77: newbyte=b"\x4D"
	if decimal==78: newbyte=b"\x4E"
	if decimal==79: newbyte=b"\x4F"
	if decimal==80: newbyte=b"\x50"
	if decimal==81: newbyte=b"\x51"
	if decimal==82: newbyte=b"\x52"
	if decimal==83: newbyte=b"\x53"
	if decimal==84: newbyte=b"\x54"
	if decimal==85: newbyte=b"\x55"
	if decimal==86: newbyte=b"\x56"
	if decimal==87: newbyte=b"\x57"
	if decimal==88: newbyte=b"\x58"
	if decimal==89: newbyte=b"\x59"
	if decimal==90: newbyte=b"\x5A"
	if decimal==91: newbyte=b"\x5B"
	if decimal==92: newbyte=b"\x5C"
	if decimal==93: newbyte=b"\x5D"
	if decimal==94: newbyte=b"\x5E"
	if decimal==95: newbyte=b"\x5F"
	if decimal==96: newbyte=b"\x60"
	if decimal==97: newbyte=b"\x61"
	if decimal==98: newbyte=b"\x62"
	if decimal==99: newbyte=b"\x63"
	if decimal==100: newbyte=b"\x64"
	if decimal==101: newbyte=b"\x65"
	if decimal==102: newbyte=b"\x66"
	if decimal==103: newbyte=b"\x67"
	if decimal==104: newbyte=b"\x68"
	if decimal==105: newbyte=b"\x69"
	if decimal==106: newbyte=b"\x6A"
	if decimal==107: newbyte=b"\x6B"
	if decimal==108: newbyte=b"\x6C"
	if decimal==109: newbyte=b"\x6D"
	if decimal==110: newbyte=b"\x6E"
	if decimal==111: newbyte=b"\x6F"
	if decimal==112: newbyte=b"\x70"
	if decimal==113: newbyte=b"\x71"
	if decimal==114: newbyte=b"\x72"
	if decimal==115: newbyte=b"\x73"
	if decimal==116: newbyte=b"\x74"
	if decimal==117: newbyte=b"\x75"
	if decimal==118: newbyte=b"\x76"
	if decimal==119: newbyte=b"\x77"
	if decimal==120: newbyte=b"\x78"
	if decimal==121: newbyte=b"\x79"
	if decimal==122: newbyte=b"\x7A"
	if decimal==123: newbyte=b"\x7B"
	if decimal==124: newbyte=b"\x7C"
	if decimal==125: newbyte=b"\x7D"
	if decimal==126: newbyte=b"\x7E"
	if decimal==127: newbyte=b"\x7F"
	if decimal==128: newbyte=b"\x80"
	if decimal==129: newbyte=b"\x81"
	if decimal==130: newbyte=b"\x82"
	if decimal==131: newbyte=b"\x83"
	if decimal==132: newbyte=b"\x84"
	if decimal==133: newbyte=b"\x85"
	if decimal==134: newbyte=b"\x86"
	if decimal==135: newbyte=b"\x87"
	if decimal==136: newbyte=b"\x88"
	if decimal==137: newbyte=b"\x89"
	if decimal==138: newbyte=b"\x8A"
	if decimal==139: newbyte=b"\x8B"
	if decimal==140: newbyte=b"\x8C"
	if decimal==141: newbyte=b"\x8D"
	if decimal==142: newbyte=b"\x8E"
	if decimal==143: newbyte=b"\x8F"
	if decimal==144: newbyte=b"\x90"
	if decimal==145: newbyte=b"\x91"
	if decimal==146: newbyte=b"\x92"
	if decimal==147: newbyte=b"\x93"
	if decimal==148: newbyte=b"\x94"
	if decimal==149: newbyte=b"\x95"
	if decimal==150: newbyte=b"\x96"
	if decimal==151: newbyte=b"\x97"
	if decimal==152: newbyte=b"\x98"
	if decimal==153: newbyte=b"\x99"
	if decimal==154: newbyte=b"\x9A"
	if decimal==155: newbyte=b"\x9B"
	if decimal==156: newbyte=b"\x9C"
	if decimal==157: newbyte=b"\x9D"
	if decimal==158: newbyte=b"\x9E"
	if decimal==159: newbyte=b"\x9F"
	if decimal==160: newbyte=b"\xA0"
	if decimal==161: newbyte=b"\xA1"
	if decimal==162: newbyte=b"\xA2"
	if decimal==163: newbyte=b"\xA3"
	if decimal==164: newbyte=b"\xA4"
	if decimal==165: newbyte=b"\xA5"
	if decimal==166: newbyte=b"\xA6"
	if decimal==167: newbyte=b"\xA7"
	if decimal==168: newbyte=b"\xA8"
	if decimal==169: newbyte=b"\xA9"
	if decimal==170: newbyte=b"\xAA"
	if decimal==171: newbyte=b"\xAB"
	if decimal==172: newbyte=b"\xAC"
	if decimal==173: newbyte=b"\xAD"
	if decimal==174: newbyte=b"\xAE"
	if decimal==175: newbyte=b"\xAF"
	if decimal==176: newbyte=b"\xB0"
	if decimal==177: newbyte=b"\xB1"
	if decimal==178: newbyte=b"\xB2"
	if decimal==179: newbyte=b"\xB3"
	if decimal==180: newbyte=b"\xB4"
	if decimal==181: newbyte=b"\xB5"
	if decimal==182: newbyte=b"\xB6"
	if decimal==183: newbyte=b"\xB7"
	if decimal==184: newbyte=b"\xB8"
	if decimal==185: newbyte=b"\xB9"
	if decimal==186: newbyte=b"\xBA"
	if decimal==187: newbyte=b"\xBB"
	if decimal==188: newbyte=b"\xBC"
	if decimal==189: newbyte=b"\xBD"
	if decimal==190: newbyte=b"\xBE"
	if decimal==191: newbyte=b"\xBF"
	if decimal==192: newbyte=b"\xC0"
	if decimal==193: newbyte=b"\xC1"
	if decimal==194: newbyte=b"\xC2"
	if decimal==195: newbyte=b"\xC3"
	if decimal==196: newbyte=b"\xC4"
	if decimal==197: newbyte=b"\xC5"
	if decimal==198: newbyte=b"\xC6"
	if decimal==199: newbyte=b"\xC7"
	if decimal==200: newbyte=b"\xC8"
	if decimal==201: newbyte=b"\xC9"
	if decimal==202: newbyte=b"\xCA"
	if decimal==203: newbyte=b"\xCB"
	if decimal==204: newbyte=b"\xCC"
	if decimal==205: newbyte=b"\xCD"
	if decimal==206: newbyte=b"\xCE"
	if decimal==207: newbyte=b"\xCF"
	if decimal==208: newbyte=b"\xD0"
	if decimal==209: newbyte=b"\xD1"
	if decimal==210: newbyte=b"\xD2"
	if decimal==211: newbyte=b"\xD3"
	if decimal==212: newbyte=b"\xD4"
	if decimal==213: newbyte=b"\xD5"
	if decimal==214: newbyte=b"\xD6"
	if decimal==215: newbyte=b"\xD7"
	if decimal==216: newbyte=b"\xD8"
	if decimal==217: newbyte=b"\xD9"
	if decimal==218: newbyte=b"\xDA"
	if decimal==219: newbyte=b"\xDB"
	if decimal==220: newbyte=b"\xDC"
	if decimal==221: newbyte=b"\xDD"
	if decimal==222: newbyte=b"\xDE"
	if decimal==223: newbyte=b"\xDF"
	if decimal==224: newbyte=b"\xE0"
	if decimal==225: newbyte=b"\xE1"
	if decimal==226: newbyte=b"\xE2"
	if decimal==227: newbyte=b"\xE3"
	if decimal==228: newbyte=b"\xE4"
	if decimal==229: newbyte=b"\xE5"
	if decimal==230: newbyte=b"\xE6"
	if decimal==231: newbyte=b"\xE7"
	if decimal==232: newbyte=b"\xE8"
	if decimal==233: newbyte=b"\xE9"
	if decimal==234: newbyte=b"\xEA"
	if decimal==235: newbyte=b"\xEB"
	if decimal==236: newbyte=b"\xEC"
	if decimal==237: newbyte=b"\xED"
	if decimal==238: newbyte=b"\xEE"
	if decimal==239: newbyte=b"\xEF"
	if decimal==240: newbyte=b"\xF0"
	if decimal==241: newbyte=b"\xF1"
	if decimal==242: newbyte=b"\xF2"
	if decimal==243: newbyte=b"\xF3"
	if decimal==244: newbyte=b"\xF4"
	if decimal==245: newbyte=b"\xF5"
	if decimal==246: newbyte=b"\xF6"
	if decimal==247: newbyte=b"\xF7"
	if decimal==248: newbyte=b"\xF8"
	if decimal==249: newbyte=b"\xF9"
	if decimal==250: newbyte=b"\xFA"
	if decimal==251: newbyte=b"\xFB"
	if decimal==252: newbyte=b"\xFC"
	if decimal==253: newbyte=b"\xFD"
	if decimal==254: newbyte=b"\xFE"
	if decimal==255: newbyte=b"\xFF"
	return(newbyte)

# Text/Character string to byte(s) string converter.
# "some_string" is any ASCII string including "\x??" characters as required.
def t2b(some_string):
	# Allocate an empty byte(s) string.
	new_byte_string=b""
	# Use the loop to build the byte(s) string from a standard string.
	for n in range(0,len(some_string),1):
		# Convert each _character_ in the string to a decimal number.
		decimal_number=ord(some_string[n])
		# Call the "d2b()" above function.
		d2b_character=d2b(decimal_number)
		# Build the byte(s) string one character at a time.
		new_byte_string=new_byte_string+d2b_character
	# The complete byte(s) string has now been converted.
	return(new_byte_string)

# End of d2b() function...
# Enjoy finding simple solutions to often very difficult problems... ;o)

# compatibility3.py

#

# Backwards compatibility for text mode Python 1.4.0 to 3.2.2...

# Some simple lines that work for all these versions on the

# classic AMIGA, E-UAE, PCLinuxOS 2009, Debian 6.0.0, Windows XP and

# Vista and WinUAE. Note, classic AMIGAs and derivatives only reach

# Python version 2.4.6. AROS goes to version 2.5.2.

# Python versions checked against, 1.4.0, 2.0.1, 2.4.2, 2.5.2, 2.6.1

# 2.6.6, 2.7.2, 3.0.1, 3.1.3 and 3.2.2.

# These are to go along with these pointers...

# http://code.activestate.com/recipes/577836-raw_input-for-all-versions-of-python/?in=lang-python

# http://code.activestate.com/recipes/577868-backwards-compatibility/?in=lang-python

# http://code.activestate.com/recipes/577872-bacwards-compatibility-part-2/?in=lang-python

# ===================================================================

# Some more ASCII print statements that work for general usage...

#

# Basic string formatting still works using Python's print function

# method using the above platforms and versions...

#

# This does NOT work for example:-

# >>> work=123.456

# >>> print("This does NOT work... ",work," ...for all versions of Python!")

#

# However these do...

print("String formatting using most of the conversion characters...")

print("Two strings to start with, see code...\n")

stringone="(C)2011, B.Walker,"

stringtwo=" G0LCU.\n"

print("%s%s" %(stringone,stringtwo))

print("A floating point number...")

somefloat=123.456

print("The floating point number is %f..." %somefloat)

print("Now a floating point number using two numbers divided by each other...")

someint=61

print("The floating point number is %f..." %(somefloat/someint))

stringone="The results are"

print("A general string, integer and floating point mixture...")

print("%s %i and %f..." %(stringone,someint,somefloat))

print("Hex %x, octal %o, decimal %d, float %f and string %s of number 61." %(someint,someint,someint,someint,str(someint)))

print("Some conversion characters might not work, '%r' is one...")

print("The next line will cause a Python error report on very early versions...")

print("This line might cause an error:- %r..." %someint)

# ===================================================================

# There will be more to come... ;o)

# Enjoy finding simple solutions to often very difficult problems. :)

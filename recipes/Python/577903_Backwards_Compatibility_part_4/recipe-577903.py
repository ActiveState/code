# compatibility4.py

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

# http://code.activestate.com/recipes/577884-backwards-compatibility-part-3/?in=lang-python

# ===================================================================

# Some more print statements that work for general usage...

# Now to print floating point and integer values using the Python

# Version 3.x.x print() function...

# (C)2011, B.Walker, G0LCU. Issued as Public Domain.

print("REMEMBER! These all work from Python 1.4.0 to 3.2.2 on")

print("Classic AMIGAs, Windows XP and Vista, PCLinuxOS 2009,")

print("Debian 6.0.0, E-UAE and WinUAE...")

print("Firstly a simple number followed by a floating point variable...")

print(36901234)

number=123.456

print(number)

print("Using + - * and / inside the 'print()' function...")

print("Two numbers added together, 123.456 + 126.544...")

print(123.456+126.544)

print("Now two numbers subtracted from each other, 123.456 - 126.544...")

print(123.456-126.544)

print("Now two numbers multiplied together 12.71 x 46.56...")

print(12.71*46.56)

print("Now two numbers divided by each other 12.71 / 46.56...")

print(12.71/46.56)

print("Now using five variables with parentheses, see code...")

numberone=123.456

numbertwo=234.567

numberthree=345.678

numberfour=456.789

# The use of parentheses do(es) not limit the universal usefulness at all...

print(((numberone+numbertwo)/(numberthree-numberfour))*number)

print("Now for a variable = 39.9 divided by an integer number 3...")

number=39.9

print(number/3)

print("Finally to print numbers and strings on screen using the line below.")

print('>>> print("The number is "+str(number/3)+"...")')

print("The number is "+str(number/3)+"...")

print("That is all for now for the 'print()' function; dead easy eh! ;o)")

# ===================================================================

# There will be more to come... ;o)

# Enjoy finding simple solutions to often very difficult problems. :)

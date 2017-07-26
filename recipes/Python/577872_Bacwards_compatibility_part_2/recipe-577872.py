# compatibility2.py
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
# ===================================================================
# Some more ASCII print statements that work for general usage...
# Remember this statement from the above pointer...
#
# "Regular expressions DO NOT work nor print statements/functions with
# variables inside."
#
# This does NOT work for example:-
# >>> work=123.456
# >>> print("This does NOT work... ",work," ...for all versions of Python!")
#
# Well this is NOT STRICTLY TRUE as there is always a way around such
# a problem.
#
# For example suppose you need to display a floating point number.
somefloat=123.456
somefloatstr=str(somefloat)
print("The floating point number is "+somefloatstr+" to 3 decimal places...")
# OR......
# ......using two text variables for the first and last parts...
textone="The floating point number is "
texttwo=" to 3 decimal places..."
print(textone+somefloatstr+texttwo)
# OR......
# ......using one of the text variables and a fixed string for the
# first and last parts.
print(textone+somefloatstr+" to 3 decimal places...")
print("\nEasy eh! ;o)\n")
# ===================================================================
# Three simple methods of displaying some random variable(s) for all
# Python versions. Therefore as long as EVERYTHING is of exactly the
# same "type()", in these cases literal strings, then they can be
# displayed in ANY text mode Python shell using the version 3.x.x
# "print()" function.
# ===================================================================
# Create a pure string from the above values.
text=textone+somefloatstr+texttwo
# So we have now proceeded to generate an ultra simple MS-DOS(TM)
# style ECHO function that works for all versions...
def echo(literalstringonly):
	# The line below does not work with 1.4.0 to 2.2.0 so ignored...
	# if isinstance(literalstringonly,str)==True: print(literalstringonly)
	# The next two lines make this function fully backwards compatible...
	checkforstring=str(type(literalstringonly))
	if checkforstring=="<type 'string'>" or checkforstring=="<type 'str'>" or checkforstring=="<class 'str'>":
		print(literalstringonly)
	else: print("Error in echo() function! Only a pure string is allowed...")
# This new echo() function now divorces itself from the print()
# function's ability to do anything but display pure strings.
# Use the new, verson independant, echo function... 
echo("This echo() function using double quotes.\r\n")
echo('This echo() function using single quotes.\r\n')
# Print the text string variable.
echo(text)
# Add a newline...
echo("")
# Adding to pure strings inside the echo() function...
text="(C)2011, B.Walker, G0LCU.\r\n"
echo(text+"Now issued as Public Domain...\r\n")
# Now test with a floating point number...
number=123.456
echo("The next line should present an error report on screen!")
echo(number)
echo("\nFinally things like echo(text[0]+text[1]+text[2]) still work, see code...")
echo(text[0]+text[1]+text[2])
# ===================================================================
# There will be more to come... ;o)
# Enjoy finding simple solutions to often very difficult problems. ;)

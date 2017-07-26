# compatibility5.py
#
# Backwards compatibility for text mode Python 2.0.1 to 3.2.2...
# Some simple things that work for all these versions on the
# classic AMIGA, E-UAE, PCLinuxOS 2009, Debian 6.0.0, Windows XP and
# Vista and WinUAE. Note, classic AMIGAs and derivatives only reach
# Python version 2.4.6. AROS goes to version 2.5.2.
# Python versions checked against, 2.0.1, 2.4.2, 2.5.2, 2.6.1, 2.6.6,
# 2.7.2, 3.0.1, 3.1.3 and 3.2.2.
#
# Versions (1.4.0), 2.0.1 to 2.7.2 have these already so running this
# code just imports "sys" only and therefore no harm is done...
#
# (C)2011, B.Walker, G0LCU. Initially issued to LXF as Public Domain.
# You may do with the code as you please.
#
# These are to go along with these pointers...
# http://code.activestate.com/recipes/577868-backwards-compatibility/?in=lang-python
# http://code.activestate.com/recipes/577872-bacwards-compatibility-part-2/?in=lang-python
# http://code.activestate.com/recipes/577884-backwards-compatibility-part-3/?in=lang-python
# http://code.activestate.com/recipes/577903-backwards-compatibility-part-4/?in=lang-python
#
# Single old functions to make Python backwards compatible... ;o)
# These are a little "tongue in cheek" but enjoy...
#
# To add to an existing Python 3.x.x run using Linux, type:-
#
# >>> exec(open('/path/to/file/compatibility5.py').read())<RETURN/ENTER>
#
# And away you go...
#
# These are a little tongue in cheek so don't take them too seriously... ;o)
# However they are functional even if a little cumbersome these days...

import sys
if sys.version[0]=="3":
	# The line "raw_input=input" has already been uploaded...
	raw_input=input
	# "xrange()" is back...
	xrange=range
	# These functions, deleted from Version 3.x.x, are now back too...
	def execfile(STRING_some_path_and_file, globals={}, locals={}):
		exec(open(STRING_some_path_and_file).read()) in globals, locals
	def reload(some_module):
		import imp
		imp.reload(some_module)
		return(some_module)
	def coerce(x,y):
		if str(type(x))=="<class 'float'>" or str(type(y))=="<class 'float'>":
			x=float(x)
			y=float(y)
		else:
			x=int(x)
			y=int(y)
		return(x,y)
# ===================================================================
# There MIGHT be more to follow, I haven't decided yet...
# Enjoy finding simple solutions to often very difficult problems... ;o)

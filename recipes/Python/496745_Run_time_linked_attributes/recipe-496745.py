""" Metaclass for making linked attributes

	The LinkedAttribute class allows you to (at run time) have objects
	that have references back to the object that created them.

	Any class that has LinkedAttribute as it's metaclass will have a
	MakedLinkedAttribute() method to make linked attributes.

	To accomplish this hackery, we use the metaclass to hijack the __init__
	method, replacing it with our own.  The new __init__ method (defined as
	Meta__init__) sets up the _creator attribute (if it was passed in) and then
	calls the original __init__ function.  The original __init__ function gets
	renamed to <class name>_old__init__.  The reason for including the class name
	in the first part of the redefinition is so that sub classes that call
	super(...).__init__ won't enter an infinite loop.
	

	The restriction to using this metaclass is that the classes that you call 
	MakeLinkedAttribute on must also have LinkedAttribute as a metaclass.

	If you use this metaclass, make sure to give credit where credit is due :)
	(e.g. in a comment or docstring)

	There are other ways of solving the same problem (including passing the
	parent to __init__ explicitly).


	The software is provided AS IS, use this software at your own risk.  There
	is no warranty.  By using this software you agree to hold the author(s)
	harmless of any damage whether direct, incidental, consequently and 
	otherwise.  In no event shall the author(s) of this code be liable for any
	damages whatsoever incurred by this code.

	(c) 2006 Michael Murr [mmurr at code-x d0t net]

"""

class LinkedAttribute(type):
	def __new__(klass, klassName, klassBases, klassDict):
		# Method to make a new linked child
		def MakeLinkedAttribute(self, childClass, *args, **kwds):
			return(childClass(_creator=self, *args, **kwds))
		# MakeLinkedAttribute(self, childClass, *args, **kwds):

		# Run time hijacking of __init__ so we can make
		# a _creator BEFORE the original __init__ is called
		#
		# We use klassName + "_hijacked__init__" so sub classes
		# who call super(...).__init__ won't enter infinite
		# loops
		#
		# Note: All your __init__ are belong to us
		def Meta__init__(self, *args, **kwds):
			# If we don't have _creator keyword do nothing
			if kwds.has_key("_creator"):
				self._creator = kwds["_creator"]
				del kwds["_creator"]
			# kwds.has_key("_creator"):

			# If we don't have an old init, do nothing
			if hasattr(self, klassName + "_hijacked__init__"):
				attr = getattr(self, klassName + "_hijacked__init__")
				attr(*args, **kwds)
			# hasattr(self, klassName + "_hijacked__init__"):
		# Meta__init__(self, *args, **kwds):

		# If we have an init, we need to save it
		if klassDict.has_key("__init__"): klassDict[klassName + "_hijacked__init__"] = klassDict["__init__"]

		# Hijack (redirect) __init__ for our [evil] purposes :)
		klassDict["__init__"] = Meta__init__
		instance = super(LinkedAttribute, klass).__new__(klass, klassName, klassBases, klassDict)
		instance.MakeLinkedAttribute = MakeLinkedAttribute

		return(instance)
	# __new__(klass, klassName, klassBases, klassDict):
# LinkedAttribute(type):

def installmethod(function, object, name = None):
	"""
	This function adds either a bound method to an instance or
	an unbound method to a class. If name is ommited it defaults
	to the name of the given function.
	Example:
	  a = A()
	  def f(self, x, y):
	    self.z = x + y
	  installmethod(f, A, "add")
	  a.add(2, 4)
	  print a.z
	  installmethod(lambda self, i: self.l[i], a, "listIndex")
	  print a.listIndex(5)
	"""
	from types import ClassType, MethodType, InstanceType
	if name == None:
		name = function.func_name
	else:
		function = renamefunction(function, name)
	if type(object) == ClassType:
		setattr(object, name,
				MethodType(function, None, object))
	elif type(object) == InstanceType:
		setattr(object, name,
				MethodType(function, object, object.__class__))
	else:
		raise TypeError

def renamefunction(function, name):
	"""
	This function returns a function identical to the given one, but
	with the given name.
	"""
	from types import FunctionType, CodeType

	c = function.func_code
	if c.co_name != name:
		# rename the code object.
		c = CodeType(c.co_argcount, c.co_nlocals, c.co_stacksize,
					 c.co_flags, c.co_code, c.co_consts,
					 c.co_names, c.co_varnames, c.co_filename,
					 name, c.co_firstlineno, c.co_lnotab)
	if function.func_defaults != None:
		return FunctionType(c, function.func_globals, name,
							function.func_defaults)
	return FunctionType(c, function.func_globals, name)


if __name__ == '__main__':
	# example
	class Widget:
		def installButton(self, name):
			def f(self, name=name):
				print name, 'pressed'
			installmethod(f, self, name)
			
	a = Widget()
	a.installButton('foo')
	a.foo()
	# AttributeError: Widget().foo()
	
	def f(self, x, y):
		self.z = x + y
	Widget.add = renamefunction(f, "add")
	a.add(2, 4)
	print a.z
	installmethod(lambda self, i: self.l[i], Widget, "listIndex")
	a.l = list("abc")
	print a.listIndex(1)
	
	# TypeError: a.add(2, 4, 6)

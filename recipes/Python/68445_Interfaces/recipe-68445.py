#
# for interface-methods non redefined in classes
#
class AbstractError:
	pass

#
# a kind of interface 
#
class Copyable:
	def copy(self):
		return self.__copy__() 
	def __interface__(self):		
		assert self.__class__.__dict__.has_key('__copy__')
		x = self.copy()
		if hasattr(self,'__cmp__') or hasattr(self,'__eq__'):						
			assert x==self
		assert x is not self
		
#
# Another kind of interface that require more elaborated 
# testing.
# __interface__ method only check that the testing stuff
# has really be done.
#
class MyStackInterface:
	def test_MyStackInterface(self, param1, param2):
		self.append(param1)
		self.append(param2)
		assert self.pop() == param2
		assert self.pop() == param1
		self.__tested = 1
	def __interface__(self):		
		assert self.__tested == 1
	def append(self, data):
		raise AbstractError
	def pop(self):
		raise AbstractError
		
		

#
#  A sample of dummy class that define our two interfaces
#
class XX(Copyable, MyStackInterface):
	def __init__(self):
		self.data = []
	def __copy__ (self):
		o = XX()
		o.data = self.data[:]
		return o
		
	def __eq__(self,other):
		return self.data == other.data
	def append(self,d):
		self.data.append(d)
	def pop(self):
		return self.data.pop()

#		
# Utilities functions for ensuring that classes well
# define interfaces.
#
def _test_interface(cl,obj):
	if cl.__dict__.has_key('__interface__'):
		cl.__interface__(obj)
	for i in cl.__bases__:
		_test_interface(i,obj)
		

def EnsureInterface(obj):
	_test_interface(obj.__class__, obj)
	

#
# and now we do the tests
#
x=XX()
x.test_MyStackInterface(0,'foo')
EnsureInterface(x)

"""
USAGE:
class A:
	__metaclass__ = Singleton
	def __init__(self):
		self.a=1
		
a=A()
b=A()
a is b #true

You don't have access to the constructor, 
you only can call a factory that returns always the same instance.
"""

_global_dict = {}

def Singleton(name, bases, namespace):
	class Result:pass
	Result.__name__ = name
	Result.__bases__ = bases
	Result.__dict__ = namespace
	_global_dict[Result] = Result()
	return Factory(Result)


class Factory:
	def __init__(self, key):
		self._key = key
	def __call__(self):
		return _global_dict[self._key]
		
def test():
	class A:
		__metaclass__ = Singleton
		def __init__(self):
			self.a=1	
	a=A()
	a1=A()
	print "a is a1", a is a1
	a.a=12
	a2=A()
	print "a.a == a2.a == 12", a.a == a2.a == 12
	class B:
		__metaclass__ = Singleton
	b=B()
	a=A()
	print "a is b",a==b

class SuperWrapper(object):
	"""Make sure descriptor super(cls) is invoked
        even when called on a class."""
	def __init__(self, cls):
		self.cls = cls
	def __get__(self, obj, cls):
		if obj is None:
			return super(self.cls, cls)
		else:
			return super(self.cls, obj)

class SuperMeta(type):
	"Automatically add attribute __sup for every class."
	def __init__(cls, name, bases, clsdict):
		setattr(cls, '_{}__sup'.format(name), SuperWrapper(cls))
		super(SuperMeta, cls).__init__(name, bases, clsdict)

# Usage examples:

class A(object):
	__metaclass__ = SuperMeta
	def meth(self):
		print 'A.meth(%s)' % self
	@classmethod
	def clsmeth(cls):
		print 'A.clsmeth(%s)' % cls

class B(A):
	def meth(self):
		self.__sup.meth()                 # super().meth()
		print 'B.meth(%s)' % self
	@classmethod
	def clsmeth(cls):
		cls.__sup.clsmeth()              # super().clsmeth()
		print 'B.clsmeth(%s)' % cls

class C(A):
	def meth(self):
		self.__sup.meth()
		print 'C.meth(%s)' % self
	@classmethod
	def clsmeth(cls):
		cls.__sup.clsmeth()
		print 'C.clsmeth(%s)' % cls

class D(B, C):
	def meth(self):
		self.__sup.meth()
		print 'D.meth(%s)' % self
	@classmethod
	def clsmeth(cls):
		cls.__sup.clsmeth()
		print 'D.clsmeth(%s)' % cls

d = D()
d.meth()
d.clsmeth()

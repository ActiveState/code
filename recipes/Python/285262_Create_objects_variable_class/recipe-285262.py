class A(object):
	def __init__(self):
		print 'This is A'
	def foo(self):
		print "foo"

class B(object):
	def __init__(self):
		print 'This is B'
	def foo(self):
		print "bar"

def getObject(cond):
	if cond:
		classname = 'A'
	else:
		classname = 'B'
	object = globals()[classname]
	return object()

myobject = getObject(1)
myobject.foo()
print dir(myobject)

print

a = A()
a.foo()
print dir(a)

print

myobject = getObject(0)
myobject.foo()
print dir(myobject)

print

b = B()
b.foo()
print dir(b)

# create blank class
print "creating empty class object"
print
class A(object):
	pass


# create hypothetical constructor
print "defining class constructor"
print "will set instance attribute \"a\""
print
def init(cls, a):
	print "initializing the instance"
	print
	cls.__setattr__("a",a)
	
	
# create new method
print """\
defining method \"show\" that takes one argument, \
a class.  It then prints class variable \"a\" and \
instance variable \"b\" \
"""
print

def show(cls):
	print "received class", cls, "as first argument"
	print "class attribute \"b\"", cls.b
	print "instnace attribute \"a\":", cls.a
	print


# add attribute to class
print "adding class attribute b=10"
print
A.b = 10


# add constructor to class
print "adding class constructor"
print "will set instance attribute \"a\""
print
A.__init__ = init


# add method to class
print "adding \"show\" method to class"
print
A.show = show


# create instance
print "creating instance \"q\" and passing \"5\" to constructor"
print
q = A(5)


# check class attribute
print "checking class attribute \"b\""
print "should equal 10"
print q.b
print


# check instance attribute
print "checking instance attribute \"a\""
print "should equal 5"
print q.a
print


# test instance method
print "testing method \"show\""
print
q.show()


# change class attribute
print "now chaning class attribute \"b\" to 30"
print
A.b = 30


# check reference to class attribute
print "checking that the class attribute changed"
print
q.show()

# direct, naive approach -- doesn't work...:
class Class1:
    def static1(name):
        print "Hello",name

# ...but now, a call such as:
Class1.static1("John")
# will fail with a TypeError, as 'static1' has become 
# an unbound-method object, not a plain function.

# This is easy to solve with a simple tiny wrapper:
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# toy-example usage:
class Class2:
    def static2(name):
        print "Hi there",name
    static2 = Callable(static2)

# now, a call such as:
Class2.static2("Peter")
# works just fine, and as-expected

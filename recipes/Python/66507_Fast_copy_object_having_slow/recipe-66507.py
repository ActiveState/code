# a function makes the idiom available
# non-invasively, everywhere:
def empty_copy(object):
    class Empty: pass
    newcopy = Empty()
    newcopy.__class__ = object.__class__
    return newcopy

# now your class can easily use this function
class YourClass:
    def __init__(self):
        print "assume there's a lot of work here"
    def __copy__(self):
        newcopy = empty_copy(self)
        print "now you can easily copy a relevant"
        print "subset of self's attributes to newcopy"

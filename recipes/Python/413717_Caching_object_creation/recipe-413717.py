# use the whatever memoize implementation you like
 
class Memoize(type):
    @memoize
    def __call__(cls, *args):
        return super(Memoize, cls).__call__(*args)

if __name__ == "__main__": # test
    
    class Object:
        __metaclass__ = Memoize
        def __init__(self, *args):
            print "object created with parameters %s" % str(args)


    o1 = Object(1) # create the first object
    o2 = Object(1) # return the already created object
    assert o1 is o2

    o3 = Object(1, 2) # create another object
    o4 = Object(1, 2) # return the already created object
    assert o3 is o4

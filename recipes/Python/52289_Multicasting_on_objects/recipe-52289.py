import operator

from UserDict import UserDict


class Multicast(UserDict):
    "Class multiplexes messages to registered objects"
    def __init__(self, objs=[]):
        UserDict.__init__(self)
        for alias, obj in objs: self.data[alias] = obj

    def __call__(self, *args, **kwargs):
        "Invoke method attributes and return results through another Multicast"
        return self.__class__( [ (alias, obj(*args, **kwargs) ) for alias, obj in self.data.items() ] )

    def __nonzero__(self):
        "A Multicast is logically true if all delegate attributes are logically true"
        return operator.truth(reduce(lambda a, b: a and b, self.data.values(), 1))

    def __getattr__(self, name):
        "Wrap requested attributes for further processing"
        return self.__class__( [ (alias, getattr(obj, name) ) for alias, obj in self.data.items() ] )

  
if __name__ == "__main__":
    import StringIO

    file1 = StringIO.StringIO()
    file2 = StringIO.StringIO()
    
    multicast = Multicast()
    multicast[id(file1)] = file1
    multicast[id(file2)] = file2

    assert not multicast.closed

    multicast.write("Testing")
    assert file1.getvalue() == file2.getvalue() == "Testing"
    
    multicast.close()
    assert multicast.closed

    print "Test complete"

    

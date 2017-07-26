def singleton(theClass):
    """ decorator for a class to make a singleton out of it """
    classInstances = {}

    def getInstance(*args, **kwargs):
        """ creating or just return the one and only class instance.
            The singleton depends on the parameters used in __init__ """
        key = (theClass, args, str(kwargs))
        if key not in classInstances:
            classInstances[key] = theClass(*args, **kwargs)
        return classInstances[key]

    return getInstance

# Example

@singleton
class A:
    """ test class """
    def __init__(self, key=None, subkey=None):
        self.key    = key
        self.subkey = subkey

    def __repr__(self):
        return "A(id=%d, %s,%s)" % (id(self), self.key, self.subkey)

def tests():
    """ some basic tests """
    testCases = [ (None, None), (10, 20), (30, None), (None, 30) ]
    instances = set()
    instance1 = None
    instance2 = None

    for key, subkey in testCases:
        if key == None:
            if subkey == None: instance1, instance2 = A(), A()
            else:              instance1, instance2 = A(subkey=subkey), A(subkey=subkey)
        else:
            if subkey == None: instance1, instance2 = A(key), A(key)
            else:              instance1, instance2 = A(key, subkey=subkey), A(key, subkey=subkey)

        print("instance1: %-25s" % instance1, " instance2: %-25s" % instance2)
        assert instance1 == instance2
        assert instance1.key == key and instance1.subkey == subkey
        instances.add(instance1)

    assert len(instances) == len(testCases)

tests()

# simple read only attributes with meta-class programming

# method factory for an attribute get method
def getmethod(attrname):
    def _getmethod(self):
        return self.__readonly__[attrname]

    return _getmethod

class metaClass(type):
    def __new__(cls,classname,bases,classdict):
        readonly = classdict.get('__readonly__',{})
        for name,default in readonly.items():
            classdict[name] = property(getmethod(name))

        return type.__new__(cls,classname,bases,classdict)

class ROClass(object):
    __metaclass__ = metaClass
    __readonly__ = {'a':1,'b':'text'}


if __name__ == '__main__':
    def test1():
        t = ROClass()
        print t.a
        print t.b

    def test2():
        t = ROClass()
        t.a = 2

    test1()

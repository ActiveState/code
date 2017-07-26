# Simple inheritance case
class super1 (object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ, *args, **kwargs)
        obj.attr1 = []
        return obj

class derived1(super1):
    def __init__(self, arg4, **kwargs):
        self.attr4 = arg4
        self.attr5 = kwargs['arg5']

if '__main__'==__name__:
    d1 = derived1(222, arg5=333)
    d1.attr1.append(111)
    print d1.attr1, d1.attr4, d1.attr5,
    print isinstance(d1, super1)

# Multiple inheritance case
class super2 (object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ, *args, **kwargs)
        obj.attr2 = 222
        return obj

import copy
class derived2 (super1, super2):
    def __new__(typ, *args, **kwargs):
        objList = [sup.__new__(typ, *args, **kwargs)
                   for sup in derived2.__bases__]
        for obj in objList[1:]:
            objList[0].__dict__.update(copy.deepcopy(obj.__dict__))
        objList[0].attr3 = 333
        return objList[0]
    def __init__(self, arg4, **kwargs):
        self.attr1.append(111)
        self.attr4 = arg4
        self.attr5 = kwargs['arg5']

if '__main__'==__name__:
    d1 = derived2(444, arg5=555)
    print d1.attr1, d1.attr2, d1.attr3, d1.attr4, d1.attr5,
    print isinstance(d1, super1),
    print isinstance(d1, super2)

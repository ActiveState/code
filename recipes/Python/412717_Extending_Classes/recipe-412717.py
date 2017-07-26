def get_obj(name): return eval(name)

class ExtendReplace(type):
    def __new__(self, name, bases, dict):
        prevclass = get_obj(name)
        del dict['__module__']
        del dict['__metaclass__']
        dict.update(prevclass.__dict__)
        ret =  type.__new__(self, name, prevclass.__bases__, dict)
        return ret

class ExtendInplace(type):
    def __new__(self, name, bases, dict):
        prevclass = get_obj(name)
        del dict['__module__']
        del dict['__metaclass__']

        # We can't use prevclass.__dict__.update since __dict__
        # isn't a real dict
        for k,v in dict.iteritems():
            setattr(prevclass, k, v)
        return prevclass

class Test:
    __metaclass__=ExtendReplace
    def test_extend1(self): return 'Test Extend 1'

ext1 = Test()
assert ext1.test()=='Test'
assert ext1.test_extend1()=='Test Extend 1'

class Test:
    __metaclass__=ExtendInplace
    def test_extend2(self): return 'Test Extend 2'

ext2 = Test()
assert ext2.test()=='Test'
assert ext2.test_extend1()=='Test Extend 1'
assert ext2.test_extend2()=='Test Extend 2'

class ReloadableClass(object):
    def __init__(self, mod_name, cls_name, *args, **kw):
        self._mod_name = mod_name
        self._cls_name = cls_name
        self._args = args
        self._kw = kw

        self._mod = __import__(mod_name)
        self._cls = getattr(self._mod, self._cls_name)

        self._obj = self._cls(*args, **kw)

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return getattr(self._obj, attr)
        raise AttributeError

    def reload(self):
        reload(self._mod)
        self._cls = getattr(self._mod, self._cls_name)

        self._obj = self._cls(*self._args, **self._kw)



# some_mod.py
class TestClass:
    def foo(self):
        print 'foo'
        #print 'bar'
    #def baz(self):
    #    print 'baz'



>>> from reloadable_class import ReloadableClass
>>> c = ReloadableClass('some_mod', 'TestClass')
>>> c.foo()
foo
>>> c.baz()
Traceback (most recent call last):
File "<stdin>", line 1, in ?
File "reloadable_class.py", line 34, in __getattribute__
    return getattr(self._obj, attr)
AttributeError: TestClass instance has no attribute 'baz'
>>> c.reload() # after making changes to TestClass
>>> c.foo()
foo
bar
>>> c.baz()
baz

import weakref, inspect

class MetaInstanceTracker(type):
    def __new__(cls, name, bases, ns):
        t = super(MetaInstanceTracker, cls).__new__(cls, name, bases, ns)
        t.__instance_refs__ = []
        return t
    def __instances__(self):
        instances = [(r, r()) for r in self.__instance_refs__]
        instances = filter(lambda (x,y): y is not None, instances)
        self.__instance_refs__ = [r for (r, o) in instances]
        return [o for (r, o) in instances]
    def __call__(self, *args, **kw):
        instance = super(MetaInstanceTracker, self).__call__(*args, **kw)
        self.__instance_refs__.append(weakref.ref(instance))
        return instance

class InstanceTracker:
    __metaclass__ = MetaInstanceTracker

class MetaAutoReloader(MetaInstanceTracker):
    def __new__(cls, name, bases, ns):
        new_class = super(MetaAutoReloader, cls).__new__(
            cls, name, bases, ns)
        f = inspect.currentframe().f_back
        for d in [f.f_locals, f.f_globals]:
            if d.has_key(name):
                old_class = d[name]
                for instance in old_class.__instances__():
                    instance.change_class(new_class)
                    new_class.__instance_refs__.append(
                        weakref.ref(instance))
                # this section only works in 2.3
                for subcls in old_class.__subclasses__():
                    newbases = ()
                    for base in subcls.__bases__:
                        if base is old_class:
                            newbases += (new_class,)
                        else:
                            newbases += (base,)
                    subcls.__bases__ = newbases
                break
        return new_class

class AutoReloader:
    __metaclass__ = MetaAutoReloader
    def change_class(self, new_class):
        self.__class__ = new_class

class Bar(AutoReloader):
    pass

class Baz(Bar):
    pass

b = Bar()
b2 = Baz()

class Bar(AutoReloader):
    def meth(self, arg):
       print arg

if __name__ == '__main__':
    # now b is "upgraded" to the new Bar class:
    b.meth(1)
    # new in 2.3, Baz instances join the fun:
    b2.meth(2)
    # new Baz() instances now play too:
    Baz().meth(3)

def adopt_class(klass, obj, *args, **kwds):
    'reclass obj to inherit klass; call __init__ with *args, **kwds'
    classname = '%s_%s' % (klass.__name__, obj.__class__.__name__)
    obj.__class__ = new.classobj(classname,  (klass, obj.__class__), {})
    klass.__init__(obj, *args, **kwds)


def demo():
    class Sandwich:
        def __init__(self, ingredients):
            self.ingredients = ingredients

        def __repr__(self):
            return reduce((lambda a,b: a+' and '+b), self.ingredients)

    class WithSpam:
        def __init__(self, spam_count):
            self.spam_count = spam_count
            
        def __repr__(self):
            return Sandwich.__repr__(self) + self.spam_count * ' and spam'

    pbs = Sandwich(['peanut butter', 'jelly'])
    adopt_class(WithSpam, pbs, 2)
    print pbs
            

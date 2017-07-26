# person.py
# Let's make a person!
from accessor import Accessorizor, make_properties, init_from_attrs

class Person(Accessorizor):
    # delcare read-only and read-write attributes
    _attrs = { 'ro'  : ('name' , 'race', 'father'), 'rw' : ('alias',  'loves') }

    def __init__(self, **kwds):
        init_from_attrs(self, kwds, class_ = Person)

make_properties(Person)

class Geek(Person):
    _attrs = {'rw': ('fav_os', 'fav_hero'), 'ro' : ('iq',)}
    def __init__(self, **kwds):
        Person.__init__(self, **kwds) # initialize superclass attributes
        init_from_attrs(self, kwds, class_ = Geek)

make_properties(Geek)

# Now let's use them
if __name__ == '__main__':
    p = Person(name = 'aragorn', race = 'man', alias = 'elessar', father = 'arathorn')

    print p.__dict__
    try:
        p.race = 'dwarf'
    except AttributeError:
        print "Can't change attribute 'race'"
    p.alias = 'strider'
    print "name = %s, alias = %s, race = %s" % (p.name, p.alias, p.race)

    p.loves = 'arwen'
    print p.__dict__

    g = Geek(name='Palin', race='dwarf', iq=200)
    print g.__dict__
    print "name = %s, race = %s" %(g.name, g.race) # test inherited attrs
    g.fav_os = 'freebsd'
    g.fav_hero = 'aragorn'
    g.loves = 'gold'
    print g.__dict__


# Under the hood ...
# accessor.py

class Accessorizor(object):
    """ A base class for classes wanting to use make_properties and init_from_attrs.
         Subclasses must have an attribute called _attrs of the form:
         { 'rw' : ('read_write_attr1', ...), 'ro': ('read_only_attr1', ...) }
    """
    ro_attrs = classmethod(lambda class_: class_._attrs['ro'])
    rw_attrs = classmethod(lambda class_: class_._attrs['rw'])

def init_from_attrs(obj, kwds, class_ = None):
    """Initialize the object using keyword args.
       If the client class C is intended to be subclassed,
       then C should be passed as the class_ parameter, otherwise
       the class_ parameter can be omitted.
    """
    if class_ is None:
        class_ = obj.__class__
    for attr in class_.ro_attrs() + class_.rw_attrs():
        attr_private = privatize(obj.__class__, attr)
        if kwds.has_key(attr):
            obj.__dict__[attr_private] = kwds[attr]
        else:
            obj.__dict__[attr_private] = None

def make_properties(class_):
    for attr in class_.rw_attrs():
        setattr(class_, attr, property(fget = make_getter(attr), fset = make_setter(attr)))
    for attr in class_.ro_attrs():
        setattr(class_, attr, property(fget = make_getter(attr)))

def make_getter(attr):
    return lambda obj: obj.__dict__[privatize(obj.__class__, attr)]

def make_setter(attr):
    def setter(obj, val): obj.__dict__[privatize(obj.__class__, attr)] = val
    return setter

def privatize(class_, attr):
    return "_%s__%s" % (class_.__name__, attr) 

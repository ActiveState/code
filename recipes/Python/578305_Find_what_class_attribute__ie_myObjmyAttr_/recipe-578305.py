import inspect
import types

def get_class(obj):
    '''Retrives the class of the given object.

    unfortunately, it seems there's no single way to query class that works in
    all cases - .__class__ doesn't work on some builtin-types, like
    re._pattern_type instances, and type() doesn't work on old-style
    classes... 
    '''
    cls = type(obj)
    if cls == types.InstanceType:
        cls = obj.__class__
    return cls

def where_attr_defined(obj, attr_name):
    '''Given an instance or class and an attribute name, returns the class
    (or instance) where it was defined, and 'how'

    If the given attribute does not exist on the object, it raises an AttributeError

    If the given attribute exists in the given instance's __dict__, it is
    simply a data attribute on the instance, and (obj, '__dict__') is returned.

    If the given attribute exists, but the method can't figure out how (perhaps
    it's some sort of builtin/func/method/attribute??), then it returns
    (obj, '(UNKNOWN)')

    Otherwise, it returns (cls, how), where cls is the class where it was defined,
    and how is one of '__dict__', '__slots__', '__getattribute__', or '__getattr__',
    or '(COMPILED)'.

    Note that in the case of __getattribute__, and __getattr__, since these
    are methods which can call super implementations, the determination of the
    exact class is tricky/imprecise.

    Details on __getattr__/__getattribute__ resolution
    --------------------------------------------------

    First of all, __getattr__/__getattribute__ are only checked if what was
    passed in was an instance, and not just a class... (because if you do
    MyClass.foo, __geattr__/__getattribute__ are not invoked!)

    If we did have an instance, and we find that one of these methods is
    defined on a class, then we call that class's implementation with the
    given attribute. If we ever get a result, we are not immediately done -
    though that class's method returned a result, it may have called a parent
    super implemenation, and that parent class's implementation is what
    "really" provided the result. So, one we have A result, we go up the
    parent chain, calling the method and getting the result for any parent
    classes which also define the method; if the attribute is ever not found,
    or the result is different than the previous, we assume the previous
    successful was the "lowest" in the chain to add support for this attribute
    name, and return that previous class.
    '''
    if not hasattr(obj, attr_name):
        raise AttributeError('%r has no attribute %r' % (obj, attr_name))
        
    if inspect.isclass(obj):
        cls = obj
        inst = None
    else:
        inst = obj
        cls = get_class(obj)
        # first try the inst's __dict__
        inst_dict = getattr(inst, '__dict__', None)
        if inst_dict is not None and attr_name in inst_dict:
            return inst, '__dict__'

    # with __dict__ and slots, we know that as soon as we find an entry,
    # that's the one that defined it...
    #
    # ...with __getattribute__ and __getattr__, it's trickier, since they're
    # classmethods, and could call the super... so even though
    # myCls.__getattr__('myAttr') could return a result, it could be calling
    # the super .__getattr__, and 'myAttr' is "acutally" added by
    # parentCls.__getattr__
    #
    # To try to resolve this, if we get a result back from one of these, we
    # don't immediately return it... instead, we continue checking up the
    # parent chain until we either fail to get a result, or get a different
    # result... Note that this isn't perferct, as (among other things), it
    # would mean that there would need to be a valid equality comparison for
    # the type of object returned...
    def find_orig_getter(start_cls, start_result, attr_name, mro, meth_name):
        # Note that we have to be fed in the mro - we can't just use
        # start_cls.mro(), as, due to diamon inheritance, it could be
        # different from the "remaining" mro of a child class...
        result_pair = (start_cls, meth_name)
        for cls in mro:
            cls_dict = getattr(cls, '__dict__', None)
            if cls_dict is not None and meth_name in cls_dict:
                getter = getattr(cls, meth_name)
                try:
                    result = getter(inst, attr_name)
                except Exception:
                    # if we didn't get a result, then whatever result
                    # we already have must be the one to use...
                    return result_pair
                else:
                    # it's possible equality comparison can return an error...
                    # so first try 'is', and then try equality in a try/except...
                    were_equal = result is start_result
                    if not were_equal:
                        try:
                            were_equal = (result == start_result)
                        except Exception:
                            # if there was an error in comparing, consider them
                            # not equal...
                            were_equal = false
                    if were_equal:
                        result_pair = (cls, meth_name)
                    else:
                        return result_pair
                        
        return result_pair

    # Go up the mro chain, checking for __dicts__, __slots__, __getattribute__, and __gettattr__
    getattr_cls = None
    # .mro attribute only exists on new-style classes, so use inspect.getmro
    mro = inspect.getmro(cls)
    for i, parent in enumerate(mro):
        cls_dict = getattr(parent, '__dict__', None)
        cls_slot = cls_dict.get('__slots__', None)
        if cls_slot is not None and attr_name in cls_slot:
            return parent, '__slots__'
        if cls_dict is not None and attr_name in cls_dict:
            return parent, '__dict__'
        for get_method in ('__getattribute__', '__getattr__'):
            if (cls_dict is not None and get_method in cls_dict
                    or cls_slot is not None and get_method in cls_slot):
                if inst is not None:
                    getter = getattr(parent, get_method)
                    try:
                        result = getter(inst, attr_name)
                    except Exception:
                        continue
                    else:
                        # we got a result - check up parent chain
                        result = find_orig_getter(parent, result, attr_name, mro[i + 1:], get_method)
                        # check that we're not just returning object.__getattribute__...
                        if result != (object, '__getattribute__'):
                            return result
    # we went all the way up the chain, and couldn't find it... 

    # if we stored a getattr result, return that...
    if getattr_cls is not None:
        return getattr_cls, '__getattr__'

    # check if the object's class is from a compiled module - if so, assume that's the source
    # of our mystery attribute
    for cls in mro:
        module = inspect.getmodule(cls)
        if module and not hasattr(module, '__file__'):
            return (cls, '(COMPILED)')

    # otherwise, we have no clue...perhaps it's some weird builtin?
    return obj, '(UNKNOWN)'


############################
# Some examples / tests... #
############################


# Helper func to print the results of where_attr_defined
def print_attr_sources(instOrCls, attrs):
    if inspect.isclass(instOrCls):
        cls = instOrCls
        inst = cls()
    else:
        inst = instOrCls 
        cls = get_class(inst)

    for attr in attrs:
        print
        for obj in (cls, inst):
            objStr = cls.__name__
            if isinstance(obj, cls):
                objStr += '()'
            print "where_attr_defined(%s, %r):" % (objStr, attr),
            try:
                print where_attr_defined(obj, attr)
            except AttributeError:
                print "!! %s does not exist !!" % attr

# Check it's behavior on new-style clases, with inheritance, 
# __slots__, and __getattr__
class MyClass(object):
    __slots__ = ['foo', 'bar']
    def __init__(self):
        self.foo = 'things'
        
    @property
    def stuff(self):
        return 'whaev'

    def __getattr__(self, attr):
        if attr == 'numberOfThyCounting':
            return 3
        raise AttributeError


class SubClass(MyClass):
    def stuff(self):
        return 'an override!'

class GrandChild(SubClass):
    def __getattr__(self, attr):
        if attr == 'deadParrot':
            return 'pining for the fjords'
        return super(GrandChild, self).__getattr__(attr)



print_attr_sources(GrandChild, ('foo', 'bar', 'stuff', '__init__', 'numberOfThyCounting',
             'deadParrot', 'santaClaus'))


# check it's behavior on old-style classes..
class OldMyClass:
    def __init__(self):
        self.foo = 'things'
        
    @property
    def stuff(self):
        return 'whaev'

    def __getattr__(self, attr):
        if attr == 'numberOfThyCounting':
            return 3
        raise AttributeError

class OldSub(OldMyClass):
    def __init__(self):
        OldMyClass.__init__(self)

print_attr_sources(OldSub, ('foo', 'stuff', 'numberOfThyCounting', '__init__'))

# Check that it works on c-compiled types...
import re
compiled = re.compile('foo')
print_attr_sources(compiled, ('pattern', 'sub'))

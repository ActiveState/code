# Only read this big ol' function if you want to know how it is implemented.
# For usage just scroll down.
def quickslice(*sliceArgs, **sliceKeys):
    """A decorator that allows for an abbreviated slice syntax in function
    arguments: {start:end}. Step is not supported. Valid quickslices are
    dictionaries with a single integer key which has an integer value.

    Arguments can be strings or integers, and indicate the positional or keyword
    arguments that should be checked for possible quickslices. By default, no
    exception is raised if the indicated arguments turn out not to be
    quickslices (consider __getitem__, which can accept slices or integers). To
    change this behavior, set the keyword argument 'argAssert' to True.

    The optional 'argSearch' keyword argument can be True or False, and
    specifies whether or not to check if *every* argument of the decorated
    function is a 'quickslice' rather than just the indicated arguments. The
    default is False.
    """
    argSearch = sliceKeys.get('argSearch', False)
    argAssert = sliceKeys.get('argAssert', False)
    
    def isqslice(arg):
        """Determine if arg is of the proper quickslice form.
        
        Proper quickslice form is a single-element dictionary whose key and
        value are both integers, like: {0:9} (key->start, value->stop)
        """
        return (isinstance(arg, dict) and len(arg) == 1 and
                isinstance(arg.keys()[0], int) and
                isinstance(arg.values()[0], int))
    
    def decorate(f):
        def _wrapper(*args, **kwargs):
            args = list(args)
            if argSearch:
                for i, arg in enumerate(args[:]):
                    if isqslice(arg):
                        start, stop = arg.popitem()
                        args[i] = slice(start, stop)
                for kw, arg in kwargs.iteritems():
                    if isqslice(arg):
                        start, stop = arg.popitem()
                        kwargs[kw] = slice(start, stop)
            elif sliceArgs:
                for arg in sliceArgs:
                    if isinstance(arg, int):
                        try:
                            if isqslice(args[arg]):
                                start, stop = args[arg].popitem()
                                args[arg] = slice(start, stop)
                            elif argAssert:
                                raise ValueError, (
                                    "argument %s expected a quickslice" % arg)
                        except (AttributeError, KeyError, IndexError):
                            pass
                    elif isinstance(arg, basestring):
                        try:
                            if isqslice(kwargs[arg]):
                                start, stop = kwargs[arg].popitem()
                                kwargs[arg] = slice(start, stop)
                            elif argAssert:
                                raise ValueError, (
                                    "argument %s expected a quickslice" % arg)
                        except (AttributeError, KeyError, IndexError):
                            pass
                    else:
                        raise TypeError, (
                            "quickslice expects integers or strings")
            return f(*args, **kwargs)
        return _wrapper
    return decorate

# These testslice functions just demonstrate the changes that will be made
# to the resulting function's arguments

# This will call the function with no changes to its arguments
@quickslice()
def testslice(*args, **kwargs):
    print args, kwargs

>>> testslice({0:5}, select={10:20})
({0: 5},) {'select': {10: 20}} # The arguments are not affected

# Argument 1 and keyword argument 'select' will be checked for quickslice
# values, and an exception will be raised if they aren't of the expected form.
# (due to argAssert)
@quickslice(1, 'select', argAssert=True)
def testslice2(*args, **kwargs):
    print args, kwargs

>>> testslice2('hello', {3:5}, select={1:2}, test={3:4})
('hello', slice(3, 5, None)) {'test': {3: 4}, 'select': slice(1, 2, None)}
# Argument 1 and keyword argument 'select' are now slices, while 'test' is
# left as is.

>>> testslice2('hello', {'yo': 3}, select=1) # Argument 1 is not a quickslice!
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "quickslice.py", line 44, in _wrapper
    raise ValueError, (
ValueError: argument 1 expected a quickslice

# Keyword arguments 'group' and 'span' will be checked for quickslices, but
# no exceptions will be raised if they turn out not to be.
@quickslice('group', 'span')
def testslice3(*args, **kwargs):
    print args, kwargs

>>> testslice3(group=1, span={10:13}) # No exception will be raised for 'group'
() {'group': 1, 'span': slice(10, 13, None)}

# argAssert is pointless here, since we are searching for quickslices. argSearch
# will take precedence.
@quickslice(argSearch=True, argAssert=True)
...

# This also doesn't make sense: telling it to expect a quickslice at the first
# argument, but also searching for quickslices in every argument. These options
# are mutually exclusive. The argSearch will take precedence.
@quickslice(0, argSearch=True)
def testslice4(*args, **kwargs):
    print args, kwargs

>>> testslice4('hello', {3:4}, {5:6}, select={7:8})
('hello', slice(3, 4, None), slice(5, 6, None)) {'select': slice(7, 8, None)}
# Everything that fits the quickslice 'protocol' is converted to a slice.

# To support dynamic function arguments, 'checked' arguments that don't actually
# exist in the function call won't raise an exception. This could also be made
# into a condition for argAssert if necessary.

from functools import partial

# Replace this with actual implementation from
# http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/
# (though this will work for simple cases)
def mro(*bases):
    return bases[0].__mro__

# This definition is only used to assist static code analyzers
def copy_ancestor_docstring(fn):
    '''Copy docstring for method from superclass

    For this decorator to work, the class has to use the `InheritableDocstrings`
    metaclass.
    '''
    raise RuntimeError('Decorator can only be used in classes '
                       'using the `InheritableDocstrings` metaclass')

def _copy_ancestor_docstring(mro, fn):
    '''Decorator to set docstring for *fn* from *mro*'''
    
    if fn.__doc__ is not None:
        raise RuntimeError('Function already has docstring')

    # Search for docstring in superclass
    for cls in mro:
        super_fn = getattr(cls, fn.__name__, None)
        if super_fn is None:
            continue
        fn.__doc__ = super_fn.__doc__
        break
    else:
        raise RuntimeError("Can't inherit docstring for %s: method does not "
                           "exist in superclass" % fn.__name__)

    return fn

class InheritableDocstrings(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        classdict = super().__prepare__(name, bases, *kwds)

        # Inject decorators into class namespace
        classdict['copy_ancestor_docstring'] = partial(_copy_ancestor_docstring, mro(*bases))
        
        return classdict

    def __new__(cls, name, bases, classdict):

        # Decorator may not exist in class dict if the class (metaclass
        # instance) was constructed with an explicit call to `type`.
        # (cf http://bugs.python.org/issue18334)            
        if 'copy_ancestor_docstring' in classdict:

            # Make sure that class definition hasn't messed with decorators
            copy_impl = getattr(classdict['copy_ancestor_docstring'], 'func', None)
            if copy_impl is not _copy_ancestor_docstring:
                raise RuntimeError('No copy_ancestor_docstring attribute may be created '
                                   'in classes using the InheritableDocstrings metaclass')
        
            # Delete decorators from class namespace
            del classdict['copy_ancestor_docstring']
        
        return super().__new__(cls, name, bases, classdict)

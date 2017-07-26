"""
Extend pickle module to allow pickling of interpreter state
including any interactively defined functions and classes.

This module is not required for unpickling such pickle files.

>>> import savestate, pickle, __main__
>>> pickle.dump(__main__, open('savestate.pickle', 'wb'), 2)
"""

import sys, pickle, new

def save_code(self, obj):
    """ Save a code object by value """
    args = (
        obj.co_argcount, obj.co_nlocals, obj.co_stacksize, obj.co_flags, obj.co_code,
        obj.co_consts, obj.co_names, obj.co_varnames, obj.co_filename, obj.co_name,
        obj.co_firstlineno, obj.co_lnotab, obj.co_freevars, obj.co_cellvars
    )
    self.save_reduce(new.code, args, obj=obj)
pickle.Pickler.dispatch[new.code] = save_code

def save_function(self, obj):
    """ Save functions by value if they are defined interactively """
    if obj.__module__ == '__main__' or obj.func_name == '<lambda>':
        args = (obj.func_code, obj.func_globals, obj.func_name, obj.func_defaults, obj.func_closure)
        self.save_reduce(new.function, args, obj=obj)
    else:
        pickle.Pickler.save_global(self, obj)
pickle.Pickler.dispatch[new.function] = save_function

def save_global_byname(self, obj, modname, objname):
    """ Save obj as a global reference. Used for objects that pickle does not find correctly. """
    self.write('%s%s\n%s\n' % (pickle.GLOBAL, modname, objname))
    self.memoize(obj)

def save_module_dict(self, obj, main_dict=vars(__import__('__main__'))):
    """ Special-case __main__.__dict__. Useful for a function's func_globals member. """
    if obj is main_dict:
        save_global_byname(self, obj, '__main__', '__dict__')
    else:
        return pickle.Pickler.save_dict(self, obj)      # fallback to original 
pickle.Pickler.dispatch[dict] = save_module_dict

def save_classobj(self, obj):
    """ Save an interactively defined classic class object by value """
    if obj.__module__ == '__main__':
        args = (obj.__name__, obj.__bases__, obj.__dict__)
        self.save_reduce(new.classobj, args, obj=obj)
    else:
        pickle.Pickler.save_global(self, obj, name)
pickle.Pickler.dispatch[new.classobj] = save_classobj

def save_instancemethod(self, obj):
    """ Save an instancemethod object """
    # Instancemethods are re-created each time they are accessed so this will not be memoized
    args = (obj.im_func, obj.im_self, obj.im_class)
    self.save_reduce(new.instancemethod, args)
pickle.Pickler.dispatch[new.instancemethod] = save_instancemethod

def save_module(self, obj):
    """ Save modules by reference, except __main__ which also gets its contents saved by value """
    if obj.__name__ == '__main__':
        self.save_reduce(__import__, (obj.__name__,), obj=obj, state=vars(obj).copy())
    elif obj.__name__.count('.') == 0:
        self.save_reduce(__import__, (obj.__name__,), obj=obj)
    else:
        save_global_byname(self, obj, *obj.__name__.rsplit('.', 1))
pickle.Pickler.dispatch[new.module] = save_module

def save_type(self, obj):
    if getattr(new, obj.__name__, None) is obj:
        # Types in 'new' module claim their module is '__builtin__' but are not actually there
        save_global_byname(self, obj, 'new', obj.__name__)
    elif obj.__module__ == '__main__':
        # Types in __main__ are saved by value

        # Make sure we have a reference to type.__new__        
        if id(type.__new__) not in self.memo:
            self.save_reduce(getattr, (type, '__new__'), obj=type.__new__)
            self.write(pickle.POP)

        # Copy dictproxy to real dict
        d = dict(obj.__dict__)
        # Clean up unpickleable descriptors added by Python
        d.pop('__dict__', None)
        d.pop('__weakref__', None)
        
        args = (type(obj), obj.__name__, obj.__bases__, d)
        self.save_reduce(type.__new__, args, obj=obj)
    else:
        # Fallback to default behavior: save by reference
        pickle.Pickler.save_global(self, obj)
pickle.Pickler.dispatch[type] = save_type

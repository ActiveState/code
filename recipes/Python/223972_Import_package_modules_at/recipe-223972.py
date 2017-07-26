###################
##                #
## classloader.py #
##                #
###################

import sys, types

def _get_mod(modulePath):
    try:
        aMod = sys.modules[modulePath]
        if not isinstance(aMod, types.ModuleType):
            raise KeyError
    except KeyError:
        # The last [''] is very important!
        aMod = __import__(modulePath, globals(), locals(), [''])
        sys.modules[modulePath] = aMod
    return aMod

def _get_func(fullFuncName):
    """Retrieve a function object from a full dotted-package name."""
    
    # Parse out the path, module, and function
    lastDot = fullFuncName.rfind(u".")
    funcName = fullFuncName[lastDot + 1:]
    modPath = fullFuncName[:lastDot]
    
    aMod = _get_mod(modPath)
    aFunc = getattr(aMod, funcName)
    
    # Assert that the function is a *callable* attribute.
    assert callable(aFunc), u"%s is not callable." % fullFuncName
    
    # Return a reference to the function itself,
    # not the results of the function.
    return aFunc

def _get_class(fullClassName, parentClass=None):
    """Load a module and retrieve a class (NOT an instance).
    
    If the parentClass is supplied, className must be of parentClass
    or a subclass of parentClass (or None is returned).
    """
    aClass = _get_func(fullClassName)
    
    # Assert that the class is a subclass of parentClass.
    if parentClass is not None:
        if not issubclass(aClass, parentClass):
            raise TypeError(u"%s is not a subclass of %s" %
                            (fullClassName, parentClass))
    
    # Return a reference to the class itself, not an instantiated object.
    return aClass


######################
##       Usage      ##
######################

class StorageManager: pass
class StorageManagerMySQL(StorageManager): pass

def storage_object(aFullClassName, allOptions={}):
    aStoreClass = _get_class(aFullClassName, StorageManager)
    return aStoreClass(allOptions)

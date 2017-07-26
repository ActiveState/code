import new
import byteplay as bp
import inspect

def persistent_locals(f):
    """Function decorator to expose local variables after execution.

    Modify the function such that, at the exit of the function
    (regular exit or exceptions), the local dictionary is copied to a
    read-only function property 'locals'.

    This decorator wraps the function in a callable object, and
    modifies its bytecode by adding an external try...finally
    statement equivalent to the following:

    def f(self, *args, **kwargs):
        try:
            ... old code ...
        finally:
            self._locals = locals().copy()
            del self._locals['self']
    """

    # ### disassemble f
    f_code = bp.Code.from_code(f.func_code)

    # ### use bytecode injection to add try...finally statement around code
    finally_label = bp.Label()
    # try:
    code_before = (bp.SETUP_FINALLY, finally_label)
    #     [original code here]
    # finally:
    code_after = [(finally_label, None),
                  # self._locals = locals().copy()
                  (bp.LOAD_GLOBAL, 'locals'),
                  (bp.CALL_FUNCTION, 0),
                  (bp.LOAD_ATTR, 'copy'),
                  (bp.CALL_FUNCTION, 0),
                  (bp.LOAD_FAST, 'self'),
                  (bp.STORE_ATTR, '_locals'),
                  #   del self._locals['self']
                  (bp.LOAD_FAST, 'self'),
                  (bp.LOAD_ATTR, '_locals'),
                  (bp.LOAD_CONST, 'self'),
                  (bp.DELETE_SUBSCR, None),
                  (bp.END_FINALLY, None),
                  (bp.LOAD_CONST, None),
                  (bp.RETURN_VALUE, None)]
    
    f_code.code.insert(0, code_before)
    f_code.code.extend(code_after)

    # ### re-assemble
    f_code.args =  ('self',) + f_code.args
    func = new.function(f_code.to_code(), f.func_globals, f.func_name,
                        f.func_defaults, f.func_closure)
                        
    return  PersistentLocalsFunction(func)


_docpostfix = """
        
This function has been decorated with the 'persistent_locals'
decorator. You can access the dictionary of the variables in the inner
scope of the function via the 'locals' attribute.

For more information about the original function, query the self._func
attribute.
"""
        
class PersistentLocalsFunction(object):
    """Wrapper class for the 'persistent_locals' decorator.

    Refer to the docstring of instances for help about the wrapped
    function.
    """
    def __init__(self, func):
        self._locals = {}
        
        # make function an instance method
        self._func = new.instancemethod(func, self, PersistentLocalsFunction)
        
        # create nice-looking doc string for the class
        signature = inspect.getargspec(func)
        signature[0].pop(0) # remove 'self' argument
        signature = inspect.formatargspec(*signature)
        
        docprefix = func.func_name + signature
        
        default_doc = '<no docstring>'
        self.__doc__ = (docprefix + '\n\n' + (func.__doc__ or default_doc)
                        + _docpostfix)
        
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
    
    @property
    def locals(self):
        return self._locals

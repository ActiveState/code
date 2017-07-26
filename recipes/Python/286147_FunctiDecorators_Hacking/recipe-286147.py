import dis, new

def _pop_funclist(f):
    """_pop_funclist(f) -> list or None

    Evaluates and returns a list constant defined at the beginning
    of a function. If the function doesn't begin with a list,
    or the list refers to parameters or other locals, a None is returned.
    The returned list is removed from the function code.
    """
    op = dis.opmap.__getitem__
    i = 0
    co = f.func_code
    s = co.co_code
    stopcodes = [op('LOAD_FAST'), op('STORE_FAST'), op('STORE_NAME'),
                  op('POP_TOP'), op('JUMP_FORWARD')]
    while i < len(s):
        code = ord(s[i])
        i += 1
        if code >= dis.HAVE_ARGUMENT:
            i += 2
        if code in stopcodes:
            return
        if code == op('BUILD_LIST') and ord(s[i]) == op('POP_TOP'):
            i += 1
            break
    else:
        return
    varname = '__func_list__'
    names = co.co_names + (varname,)
    dict_code = co.co_code[:i-1] + ''.join(map(chr, [
        op('STORE_NAME'),
        list(names).index(varname), 0,        
        op('LOAD_CONST'),
        list(co.co_consts).index(None), 0,
        op('RETURN_VALUE'),
        ]))
    func_code = chr(op('JUMP_FORWARD')) \
                + chr(i-3) + chr(0) \
                + co.co_code[3:]
    list_co = new.code(0, 0, co.co_stacksize, 64, dict_code,
                       co.co_consts, names, co.co_varnames, co.co_filename,
                       co.co_name, co.co_firstlineno, co.co_lnotab)
    func_co = new.code(co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags, func_code,
                       co.co_consts, co.co_names, co.co_varnames, co.co_filename,
                       co.co_name, co.co_firstlineno, co.co_lnotab)
    f.func_code = func_co
    globals = f.func_globals.copy()
    exec list_co in globals
    result = globals[varname]
    return result
    
def decorate(func):
    """decorate(func) -> func

    Gets the decorator list from a function and if found,
    applies the decorators in order and returns the transformed
    function.
    """    
    funclist = _pop_funclist(func)
    if funclist is None: return func
    f = func
    for d in funclist:
        if callable(d):
            f = d(f)
    return f
    

def attrs(**kw):
    def setattrs(f):
        f.__dict__.update(kw)
        return f
    return setattrs

class list_decorators(type):
    """
    Metaclass that calls the decorate function for all
    methods defined in the class.
    """
    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        for k,v in dct.iteritems():
            if hasattr(v, "func_code"):
                setattr(cls, k, decorate(v))
    
class TestClass(object):
    __metaclass__ = list_decorators

    def normal(self):
        self.x = 10

    def static(x):
        [attrs(author="shang", version=2),
         staticmethod]
        print x

    def name(cls):
        [classmethod]
        return cls.__name__


>>> TestClass.static.author
'shang'
>>> TestClass.static.version
2
>>> TestClass.name()
'TestClass'

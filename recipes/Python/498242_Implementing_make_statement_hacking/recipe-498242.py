import dis, new

def bytecode(fun):
    co = fun.func_code
    code = co.co_code
    names = co.co_names
    n = len(code)
    i = 0
    while i < n:
        end = i
        c = code[i]
        op = ord(c)
        i += 1
        oparg = None
        if op >= dis.HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i+1])*256
            i += 2
        yield (end, op, oparg)
    return


def code_all_variables_dynamic(fun):
    co = fun.func_code
    len_co_names = len(co.co_names)
    new_co_names = co.co_names + co.co_varnames
    new_co_flags = co.co_flags & ~0x02
    new_code = ''
    for end, op, arg in bytecode(fun):
        if dis.opname[op] == 'STORE_FAST':
            new_arg = arg + len_co_names
            new_code += chr(dis.opmap['STORE_NAME']) + \
                        chr(new_arg % 256) + \
                        chr(new_arg // 256)
        elif dis.opname[op] == 'LOAD_FAST':
            new_arg = arg + len_co_names
            new_code += chr(dis.opmap['LOAD_NAME']) + \
                        chr(new_arg % 256) + \
                        chr(new_arg // 256)
        else:
            if arg is None:
                new_code += chr(op)
            else:
                new_code += chr(op) + chr(arg % 256) + chr(arg // 256)
    func_co = new.code(co.co_argcount, co.co_nlocals, co.co_stacksize,
                       new_co_flags, new_code, co.co_consts, new_co_names,
                       co.co_varnames, co.co_filename, co.co_name,
                       co.co_firstlineno, co.co_lnotab,
                       co.co_freevars, co.co_cellvars)
    return func_co


# This is how make statement is implemented:
#
# make <callable> <name> <tuple>:
#     <block>
#
# @make(<callable>, <tuple>)
# def <name>():
#     <block>

def make(callable, args=()):
    def _make(fun):
        namespace = {}
        code = code_all_variables_dynamic(fun)
        eval(code, fun.func_globals, namespace)
        return callable(fun.func_name, args, namespace)
    return _make

# from PEP 359
class namespace(object):
    def __init__(self, name, args, kwargs):
        self.__dict__.update(kwargs)

@make(namespace)
def d():
    a = 10
    a = a + 1
    b = '10'
    @make(namespace)
    def e():
        w = 'xxx'


# creating a class without using the class keyword
@make(type, (dict,))
def mydict():
    def __init__(self, *args, **kwargs):
        print '__init__'
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, i, y):
        print '__setitem__(%s, %s, %s)' % (repr(self), repr(i), repr(y))
        dict.__setitem__(self, i, y)

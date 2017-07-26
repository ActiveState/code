from opcode import opmap, HAVE_ARGUMENT
globals().update(opmap)

class DataHolder(object):
    _varname_ = 'Set'
    # This varname `Set` should be treated like a reserved keyword
    # and should be used for other purpose at any scope.
    def __call__(self, **kwargs):
        if len(kwargs) != 1:
            raise TypeError(
                '%s takes exactly 1 keyword argument (%s given)'%(
                 self._varname_, len(kwargs)))
        name, value = kwargs.popitem()
        setattr(self, name, value)
        return value

def _support_testassign(f):
    co       = f.__code__
    code     = list(co.co_code)
    consts   = list(co.co_consts)
    varnames = list(co.co_varnames)
    if consts[-1] is DataHolder: # already applied
        return
    code.insert(0, LOAD_CONST)
    code.insert(1, len(consts) & 0xFF)
    code.insert(2, len(consts) >> 8)
    code.insert(3, CALL_FUNCTION)
    code.insert(4, 0 & 0xFF)
    code.insert(5, 0 >> 8)
    code.insert(6, STORE_FAST)
    code.insert(7, len(varnames) & 0xFF)
    code.insert(8, len(varnames) >> 8)

    consts.append(DataHolder)
    varnames.append(DataHolder._varname_)

    i, pos = 0, len(varnames)-1
    while i < len(code):
        opcode = code[i]
        if opcode == LOAD_GLOBAL:
            oparg = code[i+1] + (code[i+2] << 8)
            name = co.co_names[oparg]
            if name == DataHolder._varname_:
                code[i] = LOAD_FAST
                code[i+1] = pos & 0xFF
                code[i+2] = pos >> 8
        elif (opcode == CONTINUE_LOOP or
              JUMP_IF_FALSE_OR_POP <= opcode <= POP_JUMP_IF_TRUE):
            oparg = code[i+1] + (code[i+2] << 8) + 9
            code[i+1] = oparg & 0xFF
            code[i+2] = oparg >> 8
        i += 1
        if opcode >= HAVE_ARGUMENT:
            i += 2
    codeobj = type(co)(co.co_argcount, co.co_kwonlyargcount,
                       co.co_nlocals+1, co.co_stacksize, co.co_flags,
                       bytes(code), tuple(consts), co.co_names,
                       tuple(varnames), co.co_filename, co.co_name,
                       co.co_firstlineno, co.co_lnotab, co.co_freevars,
                       co.co_cellvars)
    return type(f)(codeobj, f.__globals__, f.__name__, f.__defaults__,
                    f.__closure__)

def install_testassign(mc):
    # mc can be a module or globals() dict
    from types import FunctionType
    if isinstance(mc, dict):
        d = mc
        d[DataHolder._varname_] = DataHolder()
    else:
        try:
            d = vars(mc)
        except TypeError:
            return
    for k, v in d.items():
        if v in (_support_testassign, install_testassign, DataHolder):
            continue
        if isinstance(v, FunctionType):
            newv = _support_testassign(v)
            try:
                d[k] = newv
            except TypeError:
                setattr(mc, k, newv)
        elif isinstance(v, type):
            try:
                setattr(v, DataHolder._varname_, DataHolder())
            except Exception:
                pass
            install_testassign(v)


def test_while(file):
    while Set(line=file.readline()):
        print(Set.line.rstrip())

def test_recursion(file):
    if Set(value=file.readline()):
        test_recursion(file)
        print(Set.value.rstrip())

def test_nonlocal():
    Set(x=100)
    def sub():
        Set(y=1000)
        print('inner function:', getattr(Set, 'x', 'Set has no attribute `x` in this scope'))
        print('inner function:', getattr(Set, 'y', 'Set has no attribute `y` in this scope'))
    sub()
    print('outer function:', getattr(Set, 'x', 'Set has no attribute `x` in this scope'))
    print('outer function:', getattr(Set, 'y', 'Set has no attribute `y` in this scope'))


# This should be called after all function and
# class definitions in a module.
install_testassign(globals())

# ---- Begin Test ---------

from io import StringIO
file = StringIO('\n'.join('Line no : %d'%(i+1) for i in range(5)))

print('Testing while statement:')
test_while(file)

print('\nTesting recursion:')
file.seek(0)
test_recursion(file)

print('\nTesting nonlocal scope:')
test_nonlocal()

print('\nTesting module level:')
# Using `Set` in the Module level scope can only
# be done after calling install_testassign.
file.seek(0)
while Set(line=file.readline()):
    print(Set.line.rstrip())

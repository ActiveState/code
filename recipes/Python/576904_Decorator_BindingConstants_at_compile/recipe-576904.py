from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG
globals().update(opmap)

def _make_constants(f, builtin_only=False, stoplist=[], verbose=False):
    if verbose:
        print('optimizing', f.__name__)
    try:
        co = f.__code__
    except AttributeError:
        return f        # Jython doesn't have a func_code attribute.
    newcode = list(co.co_code)
    newconsts = list(co.co_consts)
    names = co.co_names
    codelen = len(newcode)

    import builtins
    env = vars(builtins).copy()
    if builtin_only:
        stoplist = dict.fromkeys(stoplist)
        stoplist.update(f.__globals__)
    else:
        env.update(f.__globals__)

    # First pass converts global lookups into constants
    changed = False
    i = 0
    while i < codelen:
        opcode = newcode[i]
        if opcode in (EXTENDED_ARG, STORE_GLOBAL):
            return f    # for simplicity, only optimize common cases
        if opcode == LOAD_GLOBAL:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            name = co.co_names[oparg]
            if name in env and name not in stoplist:
                value = env[name]
                for pos, v in enumerate(newconsts):
                    if v is value:
                        break
                else:
                    pos = len(newconsts)
                    newconsts.append(value)
                newcode[i] = LOAD_CONST
                newcode[i+1] = pos & 0xFF
                newcode[i+2] = pos >> 8
                changed = True
                if verbose:
                    print(name, '-->', value)
        i += 1
        if opcode >= HAVE_ARGUMENT:
            i += 2

    # Second pass folds tuples of constants and constant attribute lookups
    i = 0
    while i < codelen:

        newtuple = []
        while newcode[i] == LOAD_CONST:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            newtuple.append(newconsts[oparg])
            i += 3

        opcode = newcode[i]
        if not newtuple:
            i += 1
            if opcode >= HAVE_ARGUMENT:
                i += 2
            continue

        if opcode == LOAD_ATTR:
            obj = newtuple[-1]
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            name = names[oparg]
            try:
                value = getattr(obj, name)
            except AttributeError:
                continue
            deletions = 1

        elif opcode == BUILD_TUPLE:
            oparg = newcode[i+1] + (newcode[i+2] << 8)
            if oparg != len(newtuple):
                continue
            deletions = len(newtuple)
            value = tuple(newtuple)

        else:
            continue

        reljump = deletions * 3
        newcode[i-reljump] = JUMP_FORWARD
        newcode[i-reljump+1] = (reljump-3) & 0xFF
        newcode[i-reljump+2] = (reljump-3) >> 8

        n = len(newconsts)
        newconsts.append(value)
        newcode[i] = LOAD_CONST
        newcode[i+1] = n & 0xFF
        newcode[i+2] = n >> 8
        i += 3
        changed = True
        if verbose:
            print("new folded constant:", value)

    if not changed:
        return f

    codestr = bytes(newcode)
    codeobj = type(co)(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals, co.co_stacksize,
                    co.co_flags, codestr, tuple(newconsts), co.co_names,
                    co.co_varnames, co.co_filename, co.co_name,
                    co.co_firstlineno, co.co_lnotab, co.co_freevars,
                    co.co_cellvars)
    return type(f)(codeobj, f.__globals__, f.__name__, f.__defaults__,
                    f.__closure__)

_make_constants = _make_constants(_make_constants) # optimize thyself!

def bind_all(mc, builtin_only=False, stoplist=[],  verbose=False):
    """Recursively apply constant binding to functions in a module or class.

    Use as the last line of the module (after everything is defined, but
    before test code).  In modules that need modifiable globals, set
    builtin_only to True.

    """
    from types import FunctionType, ModuleType

    def _bind_all(mc, builtin_only=False, stoplist=[],  verbose=False):

      if isinstance(mc, (ModuleType, type)):
        for k,v in list(vars(mc).items()):
          if type(v) is FunctionType:
              newv = _make_constants(v, builtin_only, stoplist,  verbose)
              setattr(mc, k, newv)
          elif isinstance(v, type):
              _bind_all(v, builtin_only, stoplist, verbose)

    if isinstance(mc, dict): # allow: bind_all(globals())
      for k,v in list(mc.items()):
        if type(v) is FunctionType:
            newv = _make_constants(v, builtin_only, stoplist,  verbose)
            mc[k] = newv
        elif isinstance(v, type):
            _bind_all(v, builtin_only, stoplist, verbose)
    else:
        _bind_all(v, builtin_only, stoplist, verbose)

@_make_constants
def make_constants(builtin_only=False, stoplist=[], verbose=False):
    """ Return a decorator for optimizing global references.

    Replaces global references with their currently defined values.
    If not defined, the dynamic (runtime) global lookup is left undisturbed.
    If builtin_only is True, then only builtins are optimized.
    Variable names in the stoplist are also left undisturbed.
    Also, folds constant attr lookups and tuples of constants.
    If verbose is True, prints each substitution as is occurs

    """
    if type(builtin_only) == type(make_constants):
        raise ValueError("The bind_constants decorator must have arguments.")
    return lambda f: _make_constants(f, builtin_only, stoplist, verbose)

## --------- Example call -----------------------------------------

import random

@make_constants(verbose=True, stoplist=['random'])
def sample(population, k):
    "Choose k unique random elements from a population sequence."

    if not isinstance(population, (list, tuple, str)):
        raise TypeError('Cannot handle type', type(population))
    n = len(population)
    if not 0 <= k <= n:
        raise ValueError("sample larger than population")
    result = [None] * k
    pool = list(population)
    for i in range(k):         # invariant:  non-selected at [0,n-i)
        j = int(random.random() * (n-i))
        result[i] = pool[j]
        pool[j] = pool[n-i-1]   # move non-selected item into vacancy
    return result


""" Output from the example call:

isinstance --> <built-in function isinstance>
list --> <class 'list'>
tuple --> <class 'tuple'>
str --> <class 'str'>
TypeError --> <class 'TypeError'>
type --> <class 'type'>
len --> <built-in function len>
ValueError --> <class 'ValueError'>
list --> <class 'list'>
range --> <class 'range'>
int --> <class 'int'>
new folded constant: (<class 'list'>, <class 'tuple'>, <class 'str'>)
"""

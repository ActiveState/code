"""
Oren Tirosh <orent@hishome.net>

Convert code objects (functions bodies only) to source code and back.
This doesn't actually decompile the bytecode - it simply fetches the
source code from the .py file and then carefully compiles it back to 
a 100% identical code object:

    c == recompile(*uncompile(c))

Not supported:
    Lambdas
    Nested functions  (you can still process the function containing them)
    Anything for which inspect.getsource can't get the source de
"""

import ast, inspect, re
from types import CodeType as code, FunctionType as function

import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))

class Error(Exception):
    pass

class Unsupported(Error):
    pass

class NoSource(Error):
    pass

def uncompile(c):
    """ uncompile(codeobj) -> [source, filename, mode, flags, firstlineno, privateprefix] """
    if c.co_flags & inspect.CO_NESTED or c.co_freevars:
        raise Unsupported('nested functions not supported')
    if c.co_name == '<lambda>':
        raise Unsupported('lambda functions not supported')
    if c.co_filename == '<string>':
        raise Unsupported('code without source file not supported')

    filename = inspect.getfile(c)
    try:
        lines, firstlineno = inspect.getsourcelines(c)
    except IOError:
        raise NoSource('source code not available')
    source = ''.join(lines)

    # __X is mangled to _ClassName__X in methods. Find this prefix:
    privateprefix = None
    for name in c.co_names:
        m = re.match('^(_[A-Za-z][A-Za-z0-9_]*)__.*$', name)
        if m:
            privateprefix = m.group(1)
            break

    return [source, filename, 'exec', c.co_flags & PyCF_MASK, firstlineno, privateprefix]

def recompile(source, filename, mode, flags=0, firstlineno=1, privateprefix=None):
    """ recompile output of uncompile back to a code object. source may also be preparsed AST """
    if isinstance(source, ast.AST):
        a = source
    else:
        a = parse_snippet(source, filename, mode, flags, firstlineno)
    node = a.body[0]
    if not isinstance(node, ast.FunctionDef):
        raise Error('Expecting function AST node')

    c0 = compile(a, filename, mode, flags, True)

    # This code object defines the function. Find the function's actual body code:
    for c in c0.co_consts:
        if not isinstance(c, code):
            continue
        if c.co_name == node.name and c.co_firstlineno == node.lineno:
            break
    else:
        raise Error('Function body code not found')

    # Re-mangle private names:
    if privateprefix is not None:

        def fixnames(names):
            isprivate = re.compile('^__.*(?<!__)$').match
            return tuple(privateprefix + name if isprivate(name) else name for name in names)

        c = code(c.co_argcount, c.co_nlocals, c.co_stacksize, c.co_flags, c.co_code, c.co_consts,
                fixnames(c.co_names), fixnames(c.co_varnames), c.co_filename, c.co_name,
                c.co_firstlineno, c.co_lnotab, c.co_freevars, c.co_cellvars)
    return c

def parse_snippet(source, filename, mode, flags, firstlineno, privateprefix_ignored=None):
    """ Like ast.parse, but accepts indented code snippet with a line number offset. """
    args = filename, mode, flags | ast.PyCF_ONLY_AST, True
    prefix = '\n'
    try:
        a = compile(prefix + source, *args)
    except IndentationError:
        # Already indented? Wrap with dummy compound statement
        prefix = 'with 0:\n'
        a = compile(prefix + source, *args)
        # peel wrapper
        a.body = a.body[0].body
    ast.increment_lineno(a, firstlineno - 2)
    return a

def test_roundtrip():
    import os

    print 'Importing everything in the medicine cabinet:'
    for filename in os.listdir(os.path.dirname(os.__file__)):
        name, ext = os.path.splitext(filename)
        if ext != '.py' or name == 'antigravity':
            continue
        try:
            __import__(name)
        except ImportError:
            pass    # some stuff in system library can't be imported
    print 'Done importing. We apologize for the noise above.\n'

    print 'Round-tripping functions to source code and back:'
    success = 0
    failed = 0
    unsupported = 0
    errors = 0

    import gc
    allfuncs = [obj for obj in gc.get_objects() if type(obj) is function]

    for func in allfuncs:
        c = func.func_code
        if type(c) is not code:
            continue    # PyPy builtin-code

        try:
            rc = recompile(*uncompile(c))
            if c == rc:
                success += 1
            else:
                failed += 1
        except Unsupported:
            unsupported += 1
        except NoSource:
            errors += 1

        print '\r%d successful roundtrip, %d failed roundtrip, %d unsupported, %d nosource ' % (success, failed, unsupported, errors),

if __name__ == '__main__':
    test_roundtrip()

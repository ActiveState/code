"""
Allow coroutines which yield in nested routines.

"""

"""
Based on the abstract syntax tree as defined in section 32 of the Python
library documentation (http://docs.python.org/lib/node892.html).
"""
from __future__ import with_statement
import _ast
class indent(object):
    def __init__(self, t):
        self.t = t
        
    def __enter__(self):
        self.t.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t.deindent()
            
class suspend_transform(object):
    def __init__(self, t, f=None):
        self.t = t
        if f is None:
            self.f = self.False
        else:
            self.f = f

    def False(self):
        return False
    
    def __enter__(self):
        self.oldtransform = self.t.transform
        self.t.transform = self.t.transform and self.f()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t.transform = self.oldtransform
        
class bracket(object):
    def __init__(self, t, l):
        assert len(l) == 2
        self.t = t
        self.l = l

    def __enter__(self):
        self.t.f.write(self.l[0])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t.f.write(self.l[1])
        
class transform(object):
    def __init__(self, ast, f, firstFunction):
        self.f = f
        if firstFunction:
            self.f.write("from __future__ import with_statement\n")
        self.ast = ast
        self._indent = ''
        self.transform = True

    def indent(self):
        self._indent = self._indent + '    '

    def deindent(self):
        self._indent=self._indent[4:]

    def write_indent(self):
        self.f.write(self._indent)

    def newline(self):
        self.f.write("\n")
        
    def newline_and_write_indent(self):
        self.newline()
        self.write_indent()
        
    def orelse(self, s):
        if s.orelse:
            self.newline_and_write_indent()
            self.write("else:")
            with indent(self):
                self.newline_and_write_indent()
                self._dispatch(s.orelse)

    def _dispatch(self, ast):
        return self.dispatch[ast.__class__](self, ast)

    def _dispatch(self, ast):
        return getattr(self, ast.__class__.__name__) (ast)
    
    def doit(self):
        self._dispatch(self.ast)
        
    def Add(self, op):    self.f.write("+")
    def And(self, boolop): self.f.write(" and ")
    def Eq(self, eq): self.f.write("==")
    def Gt(self, gt): self.f.write(">")
    def Mod(self, m): self.f.write("%")
    def GtE(self, gte): self.f.write(">+")
    def In(self, i): self.f.write(" in  ")
    def Is(self, i): self.f.write(" is ")
    def IsNot(self, isnot): self.f.write(" is not ")
    def Lt(self, lt): self.f.write("<")
    def LtE(self, lte): self.f.write("<=")
    def Mult(self, op):   self.f.write("*")
    def Not(self, op): self.f.write(" not ")
    def NotEq(self, noteq): self.f.write("!=")
    def NotIn(self, notin): self.f.write(" not in ")
    def Or(self, boolop): self.f.write(" or ")
    def Sub(self, op):    self.f.write("-")
        
    def alias(self, a):
        self.f.write(a.name)
        if a.asname:
            self.f.write(" as ")
            self.f.write(a.asname)
            
    def arguments(self, arguments):
        f = self.f
        _dispatch = self._dispatch
        write = f.write
        first = True
        for arg, default in map(None, arguments.args, arguments.defaults):
            if first:
                first = False
            else:
                write(",")
            _dispatch(arg)
            if default:
                write("=")
                _dispatch(default)
        vararg = arguments.vararg
        if vararg:
            if first:
                first = False
            else:
                write(",")
            write("*")
            write(vararg)
        kwarg = arguments.kwarg
        if kwarg:
            if first:
                first = False
            else:
                write(",")
            write("**")
            write(kwarg)

    op_dict = {
        _ast.Add: '+=',
        _ast.Sub: '-=',
        _ast.Mult: '*=',
        _ast.Div: '/=',
        _ast.Mod: '%=',
        _ast.Pow: '**=',
        _ast.RShift: '>>=',
        _ast.LShift: '<<=',
        _ast.BitOr: '|=',
        _ast.BitXor: '^=',
        _ast.BitAnd: '&=',
        }
    
    def AugAssign(self, a):
        self._dispatch(a.target)
        self.f.write(self.op_dict[a.op.__class__])
        self._dispatch(a.value)
        
    def Assert(self, a):
        self.f.write("assert ")
        self._dispatch(a.test)
        if a.msg:
            self.f.write(",")
            self._dispatch(a.msg)

    def Assign(self, assign):
        for i, target in enumerate(assign.targets):
            if i > 0:
                self.f.write(",")
            self._dispatch(target)
        self.f.write("=")
        self._dispatch(assign.value)

    def Attribute(self, attribute):
        self._dispatch(attribute.value)
        self.f.write(".")
        self.f.write(attribute.attr)

    def BinOp(self, binop):
        for p in (binop.left, binop.op, binop.right):
            self._dispatch(p)

    def BoolOp(self, boolOp):
        with bracket(self, "()"):
            first = True
            for value in boolOp.values:
                if first:
                    first = False
                else:
                    self._dispatch(boolOp.op)
                self.f.write("("); self._dispatch(value); self.f.write(")")

    def Break(self, b):
        self.f.write("break")
        
    def Call(self, call):
        def newtransform():
            if (isinstance(call.func, _ast.Name) and
                call.func.id in __builtins__):
                return False
            return True

        def transform_regular_arguments(MustBeAList):
            if MustBeAList and not call.args:
                self.f.write("tuple()")
            else:
                with bracket(self, "()"):
                    for expr in call.args:
                        if self.first:
                            self.first = False
                        else:
                            self.f.write(",")
                        self._dispatch(expr)
                    if MustBeAList and (len(call.args) == 1):
                        self.f.write(",")

        def transform_keyword_arguments():
            self.f.write(",")
            with bracket(self, "{}"):
                for i, keyword in enumerate(call.keywords):
                    if i > 0:
                        self.f.write(",")
                    self.f.write('"')
                    self.f.write(keyword.arg)
                    self.f.write('":')
                    self._dispatch(keyword.value)

        def transform_starargs():
            self.f.write(",")
            self._dispatch(call.starargs)

        def transform_kwargs():
            self.f.write(",")
            self._dispatch(call.kwargs)
            
        with suspend_transform(self, newtransform):
            self.first = True
            if self.transform:
                if (call.starargs or call.kwargs):
                    c = 'YIELD_CALL'
                elif not call.keywords:
                    c = 'YIELD_SIMPLECALL'
                else:
                    c = 'YIELD_CALL_WITH_KEYWORDS'
                self.f.write("(yield self.__class__.__metaclass__.%s,(" % c)
                self._dispatch(call.func)
                self.f.write(",")
                if c == 'YIELD_SIMPLECALL':
                    transform_regular_arguments(True)
                elif c == 'YIELD_CALL_WITH_KEYWORDS':
                    transform_regular_arguments(True)
                    transform_keyword_arguments()
                elif c == 'YIELD_CALL':
                    transform_regular_arguments(True)
                    transform_keyword_arguments()
                    transform_starargs()
                    transform_kwargs()
                self.f.write("))")
            else:
                self._dispatch(call.func)
                transform_regular_arguments(False)


    def ClassDef(self, cd):
        self.f.write("class ")
        self.f.write(cd.name)
        self.f.write("(")
        newtransform = False
        for i, base in enumerate(cd.bases):
            if i == 0:
                newtransform = base == 'coroutine'
                # not quite correct, but works in simple cases
            else:
                self.f.write(",")
            self._dispatch(base)
        self.f.write("):")
        with indent(self):
            self.newline_and_write_indent()
            self.f.write("pass")
            with suspend_transform(self):
                for stmt in cd.body:
                    self.newline_and_write_indent()
                    self._dispatch(stmt)
        self.newline()

    def Compare(self, compare):
       self._dispatch(compare.left)
       for op, expr in map(None, compare.ops, compare.comparators):
           self._dispatch(op)
           self._dispatch(expr)

    def comprehension(self, c):
        self.f.write(" for ")
        self._dispatch(c.target)
        self.f.write(" in ")
        self._dispatch(c.iter)
        for e in c.ifs:
            self._dispatch(e)
            
    def Continue(self, c):
        self.f.write("continue")
        
    def Delete(self, d):
        self.f.write("del ")
        for target in d.targets:
            self._dispatch(target)
            self.f.write(",")

    def Dict(self, d):
        with bracket(self, "{}"):
            with indent(self):
                for key, value in zip(d.keys, d.values):
                    self.newline_and_write_indent()
                    self._dispatch(key)
                    self.f.write(":")
                    self._dispatch(value)
                    self.f.write(",")
            self.newline_and_write_indent()

    def excepthandler(self, eh):
        self.newline_and_write_indent()
        self.f.write("except ")
        if eh.type:
            self._dispatch(eh.type)
        if eh.name:
            self.f.write(",")
            self._dispatch(eh.name)
        self.f.write(":")
        with indent(self):
            for b in eh.body:
                self.newline_and_write_indent()
                self._dispatch(b)

    def Exec(self, e):
        self.f.write("exec ")
        self._dispatch(e.body)
        if e.globals:
            self.f.write(" in ")
            self._dispatch(e.globals)
        if e.locals:
            self.f.write(" in ")
            self._dispatch(e.locals)

    def GeneratorExp(self, ge):
        with bracket(self, "()"):
            self._dispatch(ge.elt)
            for generator in ge.generators:
                self._dispatch(generator)
        
    def For(self, f):
        self.f.write("for ")
        self._dispatch(f.target)
        self.f.write(" in ")
        self._dispatch(f.iter)
        self.f.write(":")
        with indent(self):
            for b in f.body:
                self.newline_and_write_indent()
                self._dispatch(b)
        self.orelse(f)

    def Import(self, i):
        self.f.write("import ")
        for ind, a in enumerate(i.names):
            if ind > 0:
                self.f.write(",")
            self._dispatch(a)

    def ImportFrom(self, ia):
        self.f.write("from ")
        self.f.write(ia.module)
        self.f.write(" import ")
        for a in ia.names:
            self._dispatch(a)
        
    def Expr(self, expr):
        self._dispatch(expr.value)

    def FunctionDef(self, functiondef):
        def new_transform():
            if functiondef.name.startswith("__"):
                return False
            return len(functiondef.decorators) == 0
        
        with suspend_transform(self):
            for expr in functiondef.decorators:
                self.f.write("@")
                self_dispatch(expr)
                self.newline_and_write_indent()
        self.f.write("def ")
        self.f.write(functiondef.name)
        self.f.write("(")
        self._dispatch(functiondef.args)
        self.f.write("):")
        with indent(self):
            with suspend_transform(self, new_transform):
                # __init__ must remain a function
                for stmt in functiondef.body:
                    self.newline_and_write_indent()
                    self._dispatch(stmt)
                self.newline_and_write_indent()
                if self.transform:
                    self.f.write("yield (self.__class__.__metaclass__.YIELD_RETURN, None)")
                else:
                    self.f.write("pass")

    def Global(self, g):
        self.f.write("global ")
        self.f.write(','.join(g.names))

    def If(self, ast):
        self.f.write("if ")
        self._dispatch(ast.test)
        self.f.write(":")
        with indent(self):
            for stmt in ast.body:
                self.newline_and_write_indent()
                self._dispatch(stmt)
        if ast.orelse:
            self.newline_and_write_indent()
            self.f.write("else:")
            with indent(self):
                for stmt in ast.orelse:
                    self.newline_and_write_indent()
                    self._dispatch(stmt)
        self.newline()

    def IfExp(self, i):
        with bracket(self, "()"):
            self._dispatch(i.test)
            self.f.write(" if ")
            self._dispatch(i.body)
            self.f.write(" else ")
            self._dispatch(i.orelse)
        
    def Index(self, i):
        self._dispatch(i.value)

    def keyword(self, k):
        self.f.write(k.arg)
        self.f.write("=")
        self._dispatch(k.value)
        
    def Lambda(self, l):
        self.f.write("lambda ")
        self._dispatch(l.args)
        self.f.write(":")
        self._dispatch(l.body)

    def List(self, l):
        with bracket(self, "[]"):
            for i, e in enumerate(l.elts):
                if i > 0:
                    self.f.write(",")
                self._dispatch(e)
        
    def ListComp(self, lc):
        with bracket(self, "[]"):
            self._dispatch(lc.elt)
            for g in lc.generators:
                self._dispatch(g)
        
    def Module(self, module):
        for stmt in module.body:
            self.newline_and_write_indent()
            self._dispatch(stmt)

    def Name(self, name):
        self.f.write(name.id)

    def Num(self, num):
        self.f.write(str(num.n))
        
    def Pass(self, ast):
        self.f.write("pass")

    def Print(self, print_):
        self.f.write("print ")
        dest = print_.dest
        if dest:
            self.f.write(">>")
            self._dispatch(dest)
            first = False
        else:
            first = True
        for value in print_.values:
            if first:
                first = False
            else:
                self.f.write(",")
            self._dispatch(value)
        nl = print_.nl
        if nl:
            pass
        else:
            self.f.write(",")

    def Raise(self, r):
        self.f.write("raise ")
        if r.type:
            self._dispatch(r.type)
            if r.inst:
                self.f.write(",")
                self._dispatch(r.inst)
                if r.tback:
                    self.f.write(",")
                    self._dispatch(r.tback)
                    
    def Repr(self, r):
        with bracket(self, "``"):
            self._dispatch(r.value)
        
    def Return(self, ret):
        write = self.f.write
        value = ret.value
        if value:
            write("yield (self.__class__.__metaclass__.YIELD_RETURN,(")
            self._dispatch(value)
            write("))")
        else:
            write("(yield (self.__class__.__metaclass__.YIELD_RETURN, None))")

    def Str(self, s):
        self.f.write(repr(s.s))

    def Subscript(self, s):
        self._dispatch(s.value)
        with bracket(self, "[]"):
            self._dispatch(s.slice)

    def TryExcept(self, te):
        self.f.write("try:")
        with indent(self):
            for b in te.body:
                self.newline_and_write_indent()
                self._dispatch(b)
        with suspend_transform(self):
            for eh in te.handlers:
                self._dispatch(eh)
            self.orelse(te)

    def TryFinally(self, tf):
        with suspend_transform(self):
            self.f.write("try:")
            with indent(self):
                for b in tf.body:
                    self.newline_and_write_indent()
                    self._dispatch(b)
            self.newline_and_write_indent()
            self.f.write("finally:")
            with indent(self):
                for b in tf.finalbody:
                    self.newline_and_write_indent()
                    self._dispatch(b)
                
    def Tuple(self, t):
        with bracket(self, "()"):
            for i, exp in enumerate(t.elts):
                if i > 0:
                    self.f.write(",")
                self._dispatch(exp)
            if i == 0:
                self.f.write(",")

    def UnaryOp(self, uo):
        self._dispatch(uo.op)
        self._dispatch(uo.operand)
        
    def While(self, w):
        self.f.write("while ")
        self._dispatch(w.test)
        self.f.write(":")
        with indent(self):
            for b in w.body:
                self.newline_and_write_indent()
                self._dispatch(b)
        self.orelse(w)

    def With(self, w):
        self.f.write("with ")
        self._dispatch(w.context_expr)
        if w.optional_vars:
            self.write(" as ")
            self._dispatch(w.optional_vars)
        self.f.write(":")
        with indent(self):
            for b in w.body:
                self.newline_and_write_indent()
                self._dispatch(b)

    def Yield(self, y):
        with bracket(self, "()"):
            self.f.write("yield ")
            if y.value:
                self._dispatch(y.value)

import __future__
import _ast, inspect, string, os
from StringIO import StringIO
from types import FunctionType
from pprint import pprint

from transform_source import transform

class coroutine_metaclass(type):
    filesdir = os.path.join(os.getcwd(), "transformed")
    if not os.path.exists(filesdir):
        os.mkdir(filesdir)
    def __new__(mcl, classname, bases, classdict):
        filesdir = coroutine_metaclass.filesdir
        newdict = {}
        filename = os.path.join(filesdir, classname + ".py")
        f = file(filename, "w")
        to_replace = []
        firstFunction = True
        for key, value in classdict.items():
            newdict[key] = value
            if type(value) == FunctionType:
                is_generator_function = (value.func_code.co_flags & 0x20) != 0
                if not is_generator_function:
                    to_replace.append(key)
                    source = inspect.getsourcelines(value)
                    sourcelines = source[0]
                    firstline = sourcelines[0]
                    i = 0
                    line = sourcelines[0]
                    while line[i] in string.whitespace:
                        i += 1
                    sourcelines = [line[i:] for line in sourcelines]
                    ast = compile(''.join(sourcelines), inspect.getfile(value), 'exec', _ast.PyCF_ONLY_AST + __future__.CO_FUTURE_WITH_STATEMENT)
                    d = transform(ast, f, firstFunction).doit()
                    firstFunction = False
        f.close()
        if to_replace:
            import sys
            if sys.path[0] != filesdir:
                sys.path.insert(0, filesdir)
            if 0: import pdb; pdb.set_trace()
            replacements = __import__(classname)
            for key in to_replace:
                newdict[key] = getattr(replacements, key)
                newdict[key].transformed_by_coroutine_metaclass = True
                # Mark the transormed functions
        return super(coroutine_metaclass, mcl).__new__(mcl, classname, bases, newdict)

    YIELD_RETURN             = 0
    YIELD_SIMPLECALL         = 1
    YIELD_CALL_WITH_KEYWORDS = 2
    YIELD_CALL               = 3
    YIELD_RERAISE            = 4
    
class ReturnValue(Exception):
    def __init__(self, result, mthread):
        self.result = result
        self.mthread = mthread
        
class mthread(object):
    def __init__(self, code, args):
        self._frames = []
        self.tickactions = [None]*5
        self.tickactions[coroutine.YIELD_RETURN] = self.yieldreturn
        self.tickactions[coroutine.YIELD_SIMPLECALL]  = self.yieldsimplecall
        self.tickactions[coroutine.YIELD_CALL_WITH_KEYWORDS] = self.yieldcallWithKeywords
        self.tickactions[coroutine.YIELD_CALL] = self.yieldcall
        self.tickactions[coroutine.YIELD_RERAISE] = self.yieldreraise
        self.i = 2
        self.result = (code, args)
        self.yieldsimplecall()

    def call_common(self, code, g):
        self._frames.append(g)
        if hasattr(code, "transformed_by_coroutine_metaclass"):
            if hasattr(code, "is_generator"):
                self.i, self.result = generator_proxy(code)
            else:
                self.i, self.result = g.next()
        else:
            # regular function call
            self.i, self.result = coroutine.YIELD_RETURN, g

    def yieldsimplecall(self):
        code, args = self.result
        g = code(*args)
        self.call_common(code, g)

    def yieldreturn(self):
        self._frames.pop()
        if self._frames:
            self.i, self.result = self._frames[-1].send(self.result)
        else:
            raise ReturnValue(self.result, self)

    def yieldyield(self):
        """
        I think that we could integrate generator functions, but then the runtime would
        be quite a bit more complicated.
        """
        raise NotImplementedError

    def yieldreraise(self):
        try:
            self.i, self.result = self._frames[-1].throw(self.result.__class__, self.result)
        except Exception, ex:
            self._frames.pop()
            if self._frames:
                self.i, self.result = coroutine.YIELD_RERAISE, ex
            else:
                raise
            
    def yieldcallWithKeywords(self):
        code, regularargs, keywords = self.result
        g = code(*regularargs, **keywords)
        self.call_common(code, g)

    def yieldcall(self):
        code, args1, keywords1, args2, keywords2 = self.result
        keywords = keywords1.copy()
        keywords.update(keywords2)
        g = code(*(args1 + args2), **keywords)
        self.call_common(code, g)
        
    def tick(self):
        try:
            self.tickactions[self.i]()
        except ReturnValue:
            raise
        except Exception, ex:
            if self._frames:
                self._frames.pop()
                if self._frames:
                    self.i, self.result = coroutine.YIELD_RERAISE, ex
                else:
                    raise
            else:
                raise

class coroutine_runtime(object):
    def __init__(self):
        self.mthreads = []

    def more(self):
        return bool(self.mthreads)
    
    def call(self, method, args):
        self.mthreads.append(mthread(method, args))

    def tick(self):
        try:
            for mthread in self.mthreads:
                mthread.tick()
                
        except ReturnValue, rv:
            self.mthreads.remove(mthread)
            raise
    
class coroutine(object):
    __metaclass__ = coroutine_metaclass

def run_threads(runtime):
    try:
        while 1:
            runtime.tick()
    except ReturnValue, rv:
        return rv.result
    
def simple_call(f, args):
    """
    Shows how a coroutine can be called.
    """
    runtime = coroutine_runtime()
    runtime.call(f, args)
    while runtime.more():
        run_threads(runtime)

if __name__ == '__main__':
    # a small usage example:
    class ack(coroutine):
        def outer(self, m, n):
            result = self.ack(m, n)
            if 1:
                print "Ackermann ", m, ",", n, "=", result
        def ack(self, m, n):
            if m == 0:
                return n + 1
            if m > 0 and n == 0:
                result = self.ack(m-1, 1)
                return result
            return self.ack(m-1, self.ack(m, n-1))

    runtime = coroutine_runtime()
    
    for i, j in ( (0 , 0), (0 , 1), (1 , 0), (1 , 1), (2 , 0), (2 , 1), (3 , 0), (3 , 1), (4 , 0), (3 , 2)):
            runtime.call(ack().outer, (i, j))
    while runtime.more():
        run_threads(runtime)

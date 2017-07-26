import ast
from itertools import cycle, chain, islice
from collections import namedtuple
import operator

def explain(code_string, important=None):
    """Parse a string containing a function-like call, 
    return a namedtuple containing the results

    >>> explain('mymod.nestmod.func("arg1", "arg2", 
                                kw1="kword1", kw2="kword2",
                                *args, **kws')
    [Call(  args=['arg1', 'arg2'],
            keywords={'kw1': 'kword1', 'kw2': 'kword2'},
            starargs='args', 
            func='mymod.nestmod.func',
            kwargs='kws')]

    optional 'important' argument is a list of features to parse
    from the code_string. Features defined for a Call Node:

    args - positional arguments,
    keywords - keyword arguments,
    starargs - excess positional arguments,
    kwargs - excess keyword arguments,
    func - chained function attribute lookup.
    """

    node = ast.parse(code_string)

    visitor = StrNodeVisitor(important)

    return visitor.visit(node)

#--------------------------------------------------------------------

def attrgetter(name):
    """Get attribute 'name' from object and return
        a string representation of it."""
    getname = operator.attrgetter(name)

    def str_getattr(self, obj=None):
        obj = self if obj is None else obj
        return str(getname(obj))

    return str_getattr

def strmap(show):
    """Hardcode a particular ast Node to string representation 'show'."""
    return lambda self, node=None: show

#--------------------------------------------------------------------

class StrNodeVisitor(ast.NodeVisitor):
    """A class to return string representations of visited ast nodes."""

    visit_Name = attrgetter('id')
    visit_Num = attrgetter('n')
    visit_Str = attrgetter('s')

    # hardcoded these Nodes to return string argument when visited.
    visit_Add = strmap('+')
    visit_Sub = strmap('-')
    visit_Mult = strmap('*')
    visit_Div = strmap('/')
    visit_Mod = strmap('%')
    visit_Pow = strmap('**')
    visit_LShift = strmap('<<')
    visit_RShift = strmap('>>')
    visit_FloorDiv = strmap('//')
    visit_Not = strmap('not')
    visit_And = strmap('and')
    visit_Or = strmap('or')
    visit_Eq = strmap('==')
    visit_NotEq = strmap('!=')
    visit_Lt = strmap('<')
    visit_LtE = strmap('<=')
    visit_Gt = strmap('>')
    visit_GtE = strmap('>=')
    visit_Is = strmap('is')
    visit_IsNot = strmap('not is')
    visit_In = strmap('in')
    visit_NotIn = strmap('not in')

    def __init__(self, interested=None):
        """interested - a sequence of features of a function to
        include in returned namedtuple. Allowed features:
            func, args, keywords, starargs, kwargs"""
        try:
            self._interested = set(interested)
        except TypeError:
            self._interested = interested

    def visit_Module(self, node):
        visit = self.visit
        return [visit(body) for body in node.body]

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        """return a NamedTuple that represents a Call:
        f(arg, kw=1, *args, **kws).

        Call node defines:
            func, args, keywords, starargs, kwargs"""

        # determine which of the fields we are allowed to handle.
        defined = set(node._fields)
        try:
            interested = self._interested & defined
        except TypeError:
            interested = defined

        fields = {}
        for field in interested:

            field_contents = getattr(node, field)
            if field_contents is None:
                # short circuit if the node field is a NoneType.
                fields[field] = None
                continue

            # handle the field using one of the convenience functions.
            fields[field] = getattr(self, field)(field_contents)

        # return the result as a namedtuple rather than dict.
        BaseCallTuple = namedtuple(classname(node), interested)

        class MyCallTuple(BaseCallTuple):
            """Enable representation in a nicer string format.
            Don't use this MyCallTuple class if 'func' is not a field.
            as the string representation relies on it."""
            __str__ = CallTuple2Str

        if 'func' in interested:
            mytup = MyCallTuple(**fields)
        else:
            mytup = BaseCallTuple(**fields)

        return mytup

    def visit_List(self, node):
        """return a string representation of list."""
        return self._sequence(node, '[%s]')

    def visit_Tuple(self, node):
        """return a string representation of tuple."""
        return self._sequence(node, '(%s)')

    def visit_Dict(self, node):
        """return a string representation of a dict."""
        visit = self.visit
        keyvals = zip(node.keys, node.values)

        contents = ', '.join(['%s: %s' % (visit(key), visit(value))
                                    for key, value in keyvals])

        return '{%s}' % contents

    def visit_Attribute(self, node):
        """Attribute of form: obj.attr."""
        return '%s.%s' % (self.visit(node.value), node.attr)

    def visit_BoolOp(self, node):
        """BoolOp of form: op values
        e.g. a and b."""
        visit = self.visit

        op = ' %s ' % visit(node.op)
        return op.join([visit(n) for n in node.values])

    def visit_UnaryOp(self, node):
        """UnaryOp of form: op operand
        e.g. not []."""
        return '%(op)s %(operand)s' % dict(
                                        op=self.visit(node.op),
                                        operand=self.visit(node.operand))
    def visit_BinOp(self, node):
        """BinOp of form: left op right
        e.g. 2 * 3."""
        visit = self.visit

        return '(%(left)s %(op)s %(right)s)' % dict(
                                                    left=visit(node.left),
                                                    op=visit(node.op),
                                                    right=visit(node.right))
    def visit_Subscript(self, node):
        """Subscript of form: value[slice].
        e.g. a[1:10:2]."""
        visit = self.visit
        return '%s[%s]' % (visit(node.value), visit(node.slice))

    def visit_Slice(self, node):
        """Slice of form: lower:upper:step.
        e.g. 1:10:2."""
        visit = self.visit
        return '%s:%s:%s' % (visit(node.lower),
                                visit(node.upper), visit(node.step))

    def visit_Compare(self, node):
        """Compare of form: left ops comparators.
        e.g. x > y > z -> left=x, ops=['>', '>'], comparators=['y', 'z']
        """
        visit = self.visit

        rest = ' '.join([visit(r)
                    for r in roundrobin(node.ops, node.comparators)])
        return '%s %s' % (visit(node.left), rest)

    # Convenience functions.

    def _sequence(self, node, signature):
        visit = self.visit

        contents = ', '.join([visit(elt) for elt in node.elts])
        return signature % contents

    def func(self, func):
        """convenience function called from visit_Call."""
        return self.visit(func)

    def args(self, args):
        """convenience function called from visit_Call."""
        visit = self.visit
        return [visit(n) for n in args]

    def keywords(self, keywords):
        """convenience function called from visit_Call."""
        visit = self.visit
        return dict((kw.arg, visit(kw.value)) for kw in keywords)

    def starargs(self, starargs):
        """convenience function called from visit_Call."""
        return self.visit(starargs)

    def kwargs(self, kwargs):
        """convenience function called from visit_Call."""
        return self.visit(kwargs)

    def generic_visit(self, node):
        """Called as a fallback handler if all other visit_* functions failed.
        return '<unknown>'. if node is NoneType return ''"""
        if node is None:
            return ''
        return '<unknown: %s>' % classname(node)

#--------------------------------------------------------------------

def classname(obj):
    return obj.__class__.__name__

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def CallTuple2Str(self):
    """replacement for CallTuple's __str__ method.

    Assumes that func field is present.

    The print signature should look like:
        func(args, keywords, *starargs, **kwargs)."""

    func = self.func
    order = ['args', 'keywords', 'starargs', 'kwargs']

    # handle args.
    arg_values = getattr(self, 'args', [])
    args = ', '.join([str(arg) for arg in arg_values])

    # handle keywords.
    kw_values = getattr(self, 'keywords', {})
    keywords = ', '.join(['%s=%s' % (k, v) for k, v in kw_values.items()])

    # handle starargs.
    star = getattr(self, 'starargs', None)
    if star:
        starargs = '*%s' % star
    else:
        starargs = ''

    # handle kwargs.
    kwargs = getattr(self, 'kwargs', None)
    if kwargs:
        kwargs = '**%s' % kwargs
    else:
        kwargs = ''

    # put it all together.
    arguments = [args, keywords, starargs, kwargs]
    signature = ', '.join([arg for arg in arguments if arg != ''])
    return '%s(%s)' % (func, signature)

#--------------------------------------------------------------------

if __name__ == '__main__':

    tests = dict(
    tuple_test = "mod1.f_tuple((1,2), kw1=(1,2))",
    list_test = "f_list([1,2], kw1=[1,2])",
    dict_test = "f_dict({1:2}, kw1={1:2})",
    complex_test = "f_complex(1 + 2j, kw1=1 + 2j)",
    fn_test = "f_func(abs(-1), kw1=explain('f1(2, 3)'))",
    bool_test = "f_bool(True, False, not [], hello or 'hello')",
    slice_test = "f_slice(a[:2], b=b[1:2])",
    lambda_test = "f_lambda(lambda x: x)",
    compare_test = "f_compare(x > y > z not in [True])",
    genexp_test = "f_genexp([a for a in range(2)], b=(b for b in range(2)))")

    for name, test in tests.iteritems():
        print '%s: %s' % (name, explain(test,
                                        ['func', 'keywords', 'args'])[0])

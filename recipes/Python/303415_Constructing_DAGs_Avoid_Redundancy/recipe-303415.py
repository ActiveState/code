"""
Expr             This is a class hierarchy for representing arithmetic
  |--Atom        expressions as DAGs.  To keep the example simple, I
  |    |--Lit    have factored as much as I could into the base classes.
  |    |--Var    The most important method is Expr.__new__, which checks
  |              whether there is an existing node equivalent to the one
  |--UnOp        being constructed.  If there is, then __new__ returns
  |    |--Neg    the existing node; otherwise __new__ constructs a new
  |    |--Abs    node, then interns and returns it.
  |
  |--BinOp       For convenience, I have overloaded the arithmetic
       |--Add    operators so that they can be used to construct Exprs.
       |--Sub    E.g., something like Lit(1) + Lit(2) * -Var('x') is
       |--Mul    equivalent to Add(Lit(1), Mul(Lit(2), Neg(Var('x')))).
       |--Div    But otherwise I have kept features to a minimum.
"""

class Expr(object):
    __exprs = {}  # dict for interning nodes

    def __new__(cls, *args):
        # Get the canonical form of the node, like a hash key.  The
        # simple technique below works because nodes are constructed
        # bottom-up, so we know that the contents of args are unique.
        canonical = (cls, args)
        # Now see if an equivalent node is already interned.
        try:
            Expr.__exprs[canonical]
            print "Using existing %s node." % cls.__name__
        except KeyError:
            print "Constructing new %s node." % cls.__name__
            Expr.__exprs[canonical] = object.__new__(cls, *args)
        return Expr.__exprs[canonical]

    def __neg__(self): return Neg(self)
    def __abs__(self): return Abs(self)
    def __add__(self, r): return Add(self, r)
    def __sub__(self, r): return Sub(self, r)
    def __mul__(self, r): return Mul(self, r)
    def __div__(self, r): return Div(self, r)


class Atom(Expr):
    def __init__(self, numOrStr):
        try: self.v
        except AttributeError: self.v = numOrStr

class Lit(Atom): pass
class Var(Atom): pass


class UnOp(Expr):
    def __init__(self, operand):
        try: self.o
        except AttributeError: self.o = operand    

class Neg(UnOp): pass
class Abs(UnOp): pass


class BinOp(Expr):
    def __init__(self, left, right):
        try: self.l  # or self.r; whichever
        except AttributeError: self.l = left; self.r = right

class Add(BinOp): pass
class Sub(BinOp): pass
class Mul(BinOp): pass
class Div(BinOp): pass


# A function to count the nodes in an expression
def count_nodes(exp):
    visited = []

    def walk(exp):
        if exp in visited: return 0  # don't count nodes already visited

        visited.append(exp)
        if isinstance(exp, Atom): return 1
        elif isinstance(exp, UnOp): return 1 + walk(exp.o)
        elif isinstance(exp, BinOp): return 1 + walk(exp.l) + walk(exp.r)

    return walk(exp)

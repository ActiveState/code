import string

def make_transformer(op):
    def transform(self, other):
        return rpn_transformer(self.expr + other.expr + (op,))
    return transform

class rpn_transformer:
    __slots__ = ('expr',)

    def __init__(self, expr):
        self.expr = expr

    __mul__ = make_transformer('*')
    __div__ = make_transformer('/')
    __add__ = make_transformer('+')
    __sub__ = make_transformer('-')

names = dict((c, rpn_transformer((c,))) for c in string.ascii_lowercase)
to_postfix = lambda s: ' '.join(eval(s, names).expr)

# example

assert to_postfix('(a+b)/(c+d+e*f)-h') == 'a b + c d + e f * + / h -'

#! /usr/bin/env python
import operator

################################################################################

def evaluate(source, local):
    "Execute all math operations found in the source."
    for expression in expressions(source):
        local['_'] = tokens(expression).evaluate(local)

def expressions(source):
    "Separate expressions and yield each individually."
    lines = source.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    uncommented = map(lambda line: line.split('#', 1)[0], lines)
    for line in uncommented:
        if line and not line.isspace():
            for expression in line.split(';'):
                yield expression

def tokens(string):
    "Build an expression tree by tokenizing expression."
    evaluator = _tokens(string)
    if isinstance(evaluator, Operation) and \
       evaluator._Operation__symbol == Operation.ASSIGNMENT:
        return evaluator
    return Print(evaluator)

def _tokens(string):
    "Private module function: recursively builds a tree."
    expression = string.strip()
    if not expression:
        raise SyntaxError('empty expression')
    divisions = Operation.split(expression)
    if divisions:
        left, symbol, right = divisions
        return Operation(_tokens(left), symbol, _tokens(right))
    if len(expression.split()) > 1:
        raise SyntaxError(expression)
    if expression.startswith('0x'):
        return Constant(int(expression[2:], 16))
    if expression.startswith('0d'):
        return Constant(int(expression[2:], 10))
    if expression.startswith('0o'):
        return Constant(int(expression[2:], 8))
    if expression.startswith('0q'):
        return Constant(int(expression[2:], 4))
    if expression.startswith('0b'):
        return Constant(int(expression[2:], 2))
    if expression.isdigit():
        return Constant(int(expression))
    if expression.isidentifier():
        return Variable(expression)
    raise SyntaxError(expression)

################################################################################

class Expression:

    "Abstract class for Expression objects."

    def __init__(self):
        "Initialize the Expression object."
        raise NotImplementedError()

    def evaluate(self, bindings):
        "Calculate the value of this object."
        raise NotImplementedError()

    def __repr__(self):
        "Return a representation of this object."
        klass = self.__class__.__name__
        private = '_{}__'.format(klass)
        args = []
        for name in vars(self):
            if name.startswith(private):
                key = name[len(private):]
                value = getattr(self, name)
                args.append('{}={!r}'.format(key, value))
        return '{}({})'.format(klass, ', '.join(args))

################################################################################

class Constant(Expression):

    "Class for storing all math constants."

    def __init__(self, value):
        "Initialize the Constant object."
        self.__value = value

    def evaluate(self, bindings):
        "Calculate the value of this object."
        return self.__value

################################################################################

class Variable(Expression):

    "Class for storing all math variables."

    def __init__(self, name):
        "Initialize the Variable object."
        self.__name = name

    def evaluate(self, bindings):
        "Calculate the value of this object."
        if self.__name not in bindings:
            raise NameError(self.__name)
        return bindings[self.__name]

################################################################################

class Operation(Expression):

    "Class for executing math operations."

    ASSIGNMENT = '->'
    OPERATORS = {ASSIGNMENT: lambda a, b: None,
                 'and': lambda a, b: a and b,
                 'or': lambda a, b: a or b,
                 '+': operator.add,
                 '-': operator.sub,
                 '*': operator.mul,
                 '/': operator.floordiv,
                 '%': operator.mod,
                 '**': operator.pow,
                 '&': operator.and_,
                 '|': operator.or_,
                 '^': operator.xor,
                 '>>': operator.rshift,
                 '<<': operator.lshift,
                 '==': operator.eq,
                 '!=': operator.ne,
                 '>': operator.gt,
                 '>=': operator.ge,
                 '<': operator.lt,
                 '<=': operator.le}

    def __init__(self, left, symbol, right):
        "Initialize the Operation object."
        self.__left = left
        self.__symbol = symbol
        self.__right = right

    def evaluate(self, bindings):
        "Calculate the value of this object."
        if self.__symbol == self.ASSIGNMENT:
            if not isinstance(self.__right, Variable):
                raise TypeError(self.__right)
            key = self.__right._Variable__name
            value = self.__left.evaluate(bindings)
            bindings[key] = value
            return value
        return self.__operate(bindings)

    def __operate(self, bindings):
        "Execute operation defined by symbol."
        if self.__symbol not in self.OPERATORS:
            raise SyntaxError(self.__symbol)
        a = self.__left.evaluate(bindings)
        b = self.__right.evaluate(bindings)
        return self.OPERATORS[self.__symbol](a, b)

    __operators = sorted(OPERATORS, key=len, reverse=True)

    @classmethod
    def split(cls, expression):
        "Split expression on rightmost symbol."
        tail = cls.__split(expression)
        if tail:
            symbol, right = tail
            return expression[:-sum(map(len, tail))], symbol, right

    @classmethod
    def __split(cls, expression):
        "Private class method: help with split."
        for symbol in cls.__operators:
            if symbol in expression:
                right = expression.rsplit(symbol, 1)[1]
                tail = cls.__split(right)
                if tail is None:
                    return symbol, right
                return tail

################################################################################

class Print(Expression):

    "Class for printing all math results."

    def __init__(self, expression):
        "Initialize the Print object."
        self.__expression = expression

    def evaluate(self, bindings):
        "Calculate the value of this object."
        value = self.__expression.evaluate(bindings)
        print(value)
        return value

################################################################################

def test():
    "Run a simple demo that shows evaluator's capability."
    from sys import exc_info, stderr
    from traceback import format_exception_only
    local = {}
    while True:
        try:
            evaluate(input('>>> '), local)
        except EOFError:
            break
        except:
            stderr.write(format_exception_only(*exc_info()[:2])[-1])

if __name__ == '__main__':
    test()

class Expression:

    def __init__(self):
        raise NotImplementedError()
    
    def Evaluate(self, dictionary):
        raise NotImplementedError()

    # NEW code
    def __repr__(self):
        klass = self.__class__.__name__
        private = '_{0}__'.format(klass)
        args = []
        for name in self.__dict__:
            if name.startswith(private):
                value = self.__dict__[name]
                name = name[len(private):]
                args.append('{0}={1}'.format(name, repr(value)))
        return '{0}({1})'.format(klass, ', '.join(args))
    # END code

class Constant(Expression):

    def __init__(self, value):
        self.__value = value

    def Evaluate(self, dictionary):
        return self.__value

class Variable(Expression):

    def __init__(self, name):
        self.__name = name

    def Evaluate(self, dictionary):
        if self.__name not in dictionary:
            raise Exception('Unknown variable: ' + self.__name)
        return dictionary[self.__name]

class Operation(Expression):

    def __init__(self, left, op, right):
        self.__left = left
        self.__op = op
        self.__right = right

    def Evaluate(self, dictionary):
        # NEW code
        if self.__op == '=':
            assert isinstance(self.__left, Variable), 'Must Assign to Variable'
            name = self.__left._Variable__name
            value = self.__right.Evaluate(dictionary)
            dictionary[name] = value
            return value
        # END code
        x = self.__left.Evaluate(dictionary)
        y = self.__right.Evaluate(dictionary)
        if self.__op == '+':
            return x + y
        if self.__op == '-':
            return x - y
        if self.__op == '*':
            return x * y
        if self.__op == '/':
            return x / y
        # NEW code
        if self.__op == '//':
            return x // y
        if self.__op == '\\':
            return y / x
        if self.__op == '%':
            return x % y
        if self.__op in ('**', '^'):
            return x ** y
        if self.__op in ('and', '&&', '&'):
            return x and y
        if self.__op in ('or', '||', '|'):
            return x or y
        if self.__op == '==':
            return float(x == y)
        if self.__op == '!=':
            return float(x != y)
        if self.__op == '>':
            return float(x > y)
        if self.__op == '<':
            return float(x < y)
        if self.__op in ('>=', '=>'):
            return float(x >= y)
        if self.__op in ('<=', '=<'):
            return float(x <= y)
        # END code
        raise Exception('Unknown operator: ' + self.__op)

# NEW code
class Print(Expression):

    def __init__(self, expression):
        self.__expression = expression

    def Evaluate(self, dictionary):
        value = self.__expression.Evaluate(dictionary)
        print(value)
        return value
# END code

################################################################################

def run(string, local):
    # fix string for compatibility on all computer platforms
    string = string.replace('\r\n', '\n').replace('\r', '\n')
    lines = tokenize(string)
    build_operations(lines)
    evaluate(lines, local)

def tokenize(string):
    lines = []
    # replace ';' with line separators
    string = string.replace(';', '\n')
    # the string will be evaluate line-by-line
    for line in string.split('\n'):
        tokens = []
        # ignore empty lines and comments
        if not line or line[0] == '#':
            continue
        # tokens are separated by white-space
        for token in line.split():
            # operations are processed later
            if token in ('=', '+', '-', '*', '/', '//', '\\', '%',
                         '**', '^', 'and', '&&', '&', 'or', '||', '|',
                         '==', '!=', '>', '<', '>=', '=>', '<=', '=<'):
                tokens.append(token)
            else:
                try:
                    # the token is a constant if it can be converted to a float
                    tokens.append(Constant(float(token)))
                except:
                    # ... otherwise we assume that it is a variable
                    tokens.append(Variable(token))
        lines.append(tokens)
    return lines

def build_operations(lines):
    # now we work on sorting through operations
    for line_index, line in enumerate(lines):
        # assignment is optional on a line
        if '=' in line:
            # split on '=' so each section can be processed
            tokens = split(line)
            # single variables must be on the left of '='
            for section in tokens[:-1]:
                assert len(section) == 1, 'Must Have Single Token'
                assert isinstance(section[0], Variable), 'Must Assign to Variable'
            # construct an operation from the last tokens
            tokens[-1] = flatten(tokens[-1])
            # create as many assignment operations as needed
            op = Operation(tokens[-2][0], '=', tokens[-1])
            for token_index in range(len(tokens) - 3, -1, -1):
                op = Operation(tokens[token_index][0], '=', op)
            # replace the line with the final operation
            lines[line_index] = op
        else:
            # no assignment? assume evaluation and printing
            op = flatten(line)
            lines[line_index] = Print(op)
            
def split(line):
    # split the tokens in the line on '='
    tokens = []
    while '=' in line:
        index = line.index('=')
        tokens.append(line[:index])
        line = line[index+1:]
    return tokens + [line]

def flatten(tokens):
    # check for odd number of tokens
    assert len(tokens) % 2 == 1, 'Must Have Odd Number of Tokens'
    toggle = True
    # check the token construction sequence
    for token in tokens:
        if toggle:
            assert isinstance(token, (Constant, Variable)), 'Must Have Constant or Variable'
        else:
            assert isinstance(token, str), 'Must Have Operation'
        toggle = not toggle
    # if there is only one token, it does not need to be flattened
    if len(tokens) == 1:
        return tokens[0]
    # construct the needed operations starting from the beginning
    op = Operation(*tokens[:3])
    for index in range(3, len(tokens), 2):
        op = Operation(op, tokens[index], tokens[index+1])
    return op

def evaluate(lines, local):
    # evaluate the lines in order with the local dictionary
    for line in lines:
        local['_'] = line.Evaluate(local)

################################################################################

def test():
    import sys
    local = {}
    while True:
        try:
            run(input('>>> '), local)
        except EOFError:
            return
        except Exception as err:
            sys.stderr.write(err.args[0] + '\n')

if __name__ == '__main__':
    test()

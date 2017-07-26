class Stack:
    def __init__(self):
        self.data = []
    def push(self, x):
        self.data.append(x)
    def pop(self):
        return self.data.pop()
class Interpreter:

    def __init__(self):
        self.stack = Stack()

    def process(self, word):
        if is_int(word):
            n = int(word)
            self.stack.push(n)
        elif '"' in word:
            self.stack.push(word.strip('"'))
        else:
            try:
                f = words[word]
            except KeyError:
                raise SyntaxError, 'ERRor Unknown word\n\t'+word+'!!!'

            # determine number of arguments
            n = num_args(f)

            # pop that number of args from stack
            args = reversed([self.stack.pop() for i in range(n)])

            # call f with that list
            result = f(*args)

            # take return value (a list)
            # push elements on stack
            for x in result or []:
                self.stack.push(x)

    def process_line(self, line):
        words = line.split()
        for word in words:
            self.process(word)
def _print(x):
    print x
def _pas():
    pass
def _exit():
    exit()
        
def _help():
    print '''
    words = {
    '+': lambda x, y: [x+y],
    '-': lambda x, y: [x-y],
    '*': lambda x, y: [x*y],
    '/': lambda x, y: [x/y],
    '==': lambda x, y: [x==y],
    '!=': lambda x, y: [x!=y],
    '>': lambda x, y: [x>y],
    '<': lambda x, y: [x<y],
    'dup': lambda x: [x, x],
    'drop': lambda x: [],
    'swap': lambda x, y: [y, x],
    'print': _print,
    'chr': lambda x: [chr(x)],
    'sweep': _pas,
    'scan': lambda x: [raw_input(x)],
    'exit': _exit,
    'help': _help
    }
    '''
words = {
    '+': lambda x, y: [x+y],
    '-': lambda x, y: [x-y],
    '*': lambda x, y: [x*y],
    '/': lambda x, y: [x/y],
    '==': lambda x, y: [x==y],
    '!=': lambda x, y: [x!=y],
    '>': lambda x, y: [x>y],
    '<': lambda x, y: [x<y],
    'dup': lambda x: [x, x],
    'drop': lambda x: [],
    'swap': lambda x, y: [y, x],
    'print': _print,
    'chr': lambda x: [chr(x)],
    'sweep': _pas,
    'scan': lambda x: [raw_input(x)],
    'exit': _exit,
    'help': _help,
    '.': _pas
    
}
def num_args(f):
    """ Return the number of arguments that function <f> takes. """
    return f.func_code.co_argcount

def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True
if __name__ == "__main__":
    import sys
    e = Interpreter()
    main = True
    print '==================================================='
    print '***************************************************'
    print 'drinkable_chicken modified version 1.0.0 6.13.2013'
    print 'A.W.T. 10 YRS. old'
    print '***************************************************'
    print 'IDE 1.0.1'
    print '==================================================='
    while main == True:
        line = raw_input('> ')
        if '.' in line:
            e.process_line(line)
            if 'sweep' in line:
                e.stack.data = []
            print "stack:", e.stack.data
        else:
            print 'ERRor command \n\tterminator not found!'
    

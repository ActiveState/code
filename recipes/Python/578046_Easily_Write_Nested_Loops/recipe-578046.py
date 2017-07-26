"""Provide an iterator for automatically nesting multiple sequences.

The "nest" generator function in this module is provided to make writing
nested loops easier to accomplish. Instead of writing a for loop at each
level, one may call "nest" with each sequence as an argument and receive
items from the sequences correctly yielded back to the caller. A test is
included at the bottom of this module to demonstrate how to use the code."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '17 February 2012'
__version__ = 1, 0, 0

################################################################################

def nest(*iterables):
    "Iterate over the iterables as if they were nested in loops."
    return _nest(list(map(tuple, reversed(iterables))))

def _nest(stack):
    "Build recursive loops and iterate over tuples on the stack."
    top = stack.pop()
    if stack:
        for v1 in top:
            for v2 in _nest(stack):
                yield (v1,) + v2
    else:
        for value in top:
            yield (value,)
    stack.append(top)

################################################################################

def test():
    "Check the nest generator function for correct yield values."
    subject = 'I He She It They Adam Eve Cain Abel Zacharias'.split()
    verb = 'ate bought caught dangled elected fought got hit'.split()
    complement = 'an elephant,a cow,the boot,my gun,its head'.split(',')
    for sentence in nest(subject, verb, complement):
        print('{} {} {}.'.format(*sentence))

if __name__ == '__main__':
    test()

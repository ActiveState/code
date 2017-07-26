import types

__docformat__ = "restructuredtext"


def walk_recursive_generators(generator):

    """Walk a tree of generators without yielding things recursively.

    Let's suppose you have this:

    >>> def generator0():
    ...     yield 3
    ...     yield 4
    ... 
    >>> def generator1():
    ...     yield 2
    ...     for i in generator0():
    ...         yield i
    ...     yield 5
    ... 
    >>> def generator2():
    ...     yield 1
    ...     for i in generator1():
    ...         yield i
    ...     yield 6
    ... 
    >>> for i in generator2():
    ...     print i
    ... 
    1
    2
    3
    4
    5
    6

    Notice the way the generators are recursively yielding values.  This
    library uses a technique called "bounce" that is usually used to
    implement stackless interpreters.  It lets you write:

    >>> def generator0():
    ...     yield 3
    ...     yield 4
    ... 
    >>> def generator1():
    ...     yield 2
    ...     yield generator0()
    ...     yield 5
    ... 
    >>> def generator2():
    ...     yield 1
    ...     yield generator1()
    ...     yield 6
    ... 
    >>> for i in walk_recursive_generators(generator2()):
    ...     print i
    ... 
    1
    2
    3
    4
    5
    6

    Look Ma!  No recursive yields!

    """

    stack = [generator]
    while stack:
        for x in stack[-1]:
            if isinstance(x, types.GeneratorType):
                stack.append(x)  # Recurse.
                break
            else:
                yield x
        else:
            stack.pop()


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()

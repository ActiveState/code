def function(a, b):
    # description and test
    """Adds an integer and a float and returns a str.
    >>> function(1, 3.0)
    '4.0'
    """

    # precondition
    assert isinstance(a, int), 'a argument should be int'
    assert isinstance(b, float), 'b argument should be float'

    #implementation
    try:
        c = str(a + b)
        return c

    # postcondition
    finally:
        assert isinstance(c, str), 'c variable should be str'


# run all docstring test on debug mode
if __debug__:
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    # do something
    pass

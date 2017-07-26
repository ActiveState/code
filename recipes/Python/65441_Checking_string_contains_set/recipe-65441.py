def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]

def containsAll(str, set):
    """Check whether 'str' contains ALL of the chars in 'set'"""
    return 0 not in [c in str for c in set]

if __name__ == "__main__":
    # unit tests, must print "OK!" when run
    assert containsAny('*.py', '*?[]')
    assert not containsAny('file.txt', '*?[]')
    assert containsAll('43221', '123')
    assert not containsAll('134', '123')
    print "OK!"

def pfunc(inputfields, operation):
    """Parameterized computation of a new field
    
    For example, append a field that is the sum of fields 1 and 3:
    >>> z = pfunc((1, 3), operator.add)
    >>> database = [(10, 25, 30, 40, 50, 60), (100, 250, 300, 10, 500, 600)]
    >>> map(z, database)
    [(10, 25, 30, 40, 50, 60, 65), (100, 250, 300, 10, 500, 600, 260)]
    """
    def z(record):
        newfield = operation(*[record[f] for f in inputfields])
        return record + (newfield,)
    return z

def rfunc(inputfield, operation):
    """Parameterized reduce operation
    
    For example, find the maximum value of field 2:
    >>> r = rfunc(2, max)
    >>> database = [(10, 25, 30, 40, 50, 60), (100, 250, 300, 10, 500, 600)]
    >>> reduce(r, database, 0)
    300
    """
    def z(cumval, record):
        x = record[inputfield]
        return operation(cumval, x)
    return z

def filt_func(inputfields, operation):
    """Parameterized filter operation

    For example, get records where field1 < field3:
    >>> f = filt_func((1, 3), operator.lt)
    >>> database = [(10, 25, 30, 40, 50, 60), (100, 250, 300, 10, 500, 600)]    
    >>> filter(f, database)
    [(10, 25, 30, 40, 50, 60)]
    """
    def z(record):
        i, j = inputfields
        return operation(record[i], record[j])
    return z

def xfunc(fields):
    """Parameterized extract operation

    For example, extract fields 1, 3, and 4
    >>> x = xfunc((1,3,4))
    >>> database = [(10, 25, 30, 40, 50, 60), (100, 250, 300, 10, 500, 600)]     
    >>> map(x, database)
    [(25, 40, 50), (250, 10, 500)]
    """
    def z(record):
        return tuple([record[f] for f in fields])
    return z


# Test the examples
if  __name__ == '__main__':
    import doctest, operator
    doctest.testmod()

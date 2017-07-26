def non_exp_repr(x):
    """Return a floating point representation without exponential notation.

    Result is a string that satisfies:
        float(result)==float(x) and 'e' not in result.
    
    >>> non_exp_repr(1.234e-025)
    '0.00000000000000000000000012339999999999999'
    >>> non_exp_repr(-1.234e+018)
    '-1234000000000000000.0'
    
    >>> for e in xrange(-50,51):
    ...     for m in (1.234, 0.018, -0.89, -75.59, 100/7.0, -909):
    ...         x = m * 10 ** e
    ...         s = non_exp_repr(x)
    ...         assert 'e' not in s
    ...         assert float(x) == float(s)

    """
    s = repr(float(x))
    e_loc = s.lower().find('e')
    if e_loc == -1:
        return s

    mantissa = s[:e_loc].replace('.', '')
    exp = int(s[e_loc+1:])

    assert s[1] == '.' or s[0] == '-' and s[2] == '.', "Unsupported format"     
    sign = ''
    if mantissa[0] == '-':
        sign = '-'
        mantissa = mantissa[1:]

    digitsafter = len(mantissa) - 1     # num digits after the decimal point
    if exp >= digitsafter:
        return sign + mantissa + '0' * (exp - digitsafter) + '.0'
    elif exp <= -1:
        return sign + '0.' + '0' * (-exp - 1) + mantissa
    ip = exp + 1                        # insertion point
    return sign + mantissa[:ip] + '.' + mantissa[ip:]


if __name__ == '__main__':
    import doctest
    print 'Doctest results:', doctest.testmod()

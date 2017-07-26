def isabn(obj):
    """isabn(string or int) -> True|False

    Validate an ABN (Australian Business Number).
    http://www.ato.gov.au/businesses/content.asp?doc=/content/13187.htm

    Accepts an int or a string of exactly 11 digits and no leading zeroes.
    Digits may be optionally separated with spaces. Any other input raises
    TypeError or ValueError.

    Return True if the argument is a valid ABN, otherwise False.

    >>> isabn('53 004 085 616')
    True
    >>> isabn('93 004 085 616')
    False

    """
    if isinstance(obj, int):
        if not 10**10 <= obj < 10**11:
            raise ValueError('int out of range for an ABN')
        obj = str(obj)
        assert len(obj) == 11
    if not isinstance(obj, str):
        raise TypeError('expected a str or int but got %s' % type(obj))
    obj = obj.replace(' ', '')
    if len(obj) != 11:
        raise ValueError('ABN must have exactly 11 digits')
    if not obj.isdigit():
        raise ValueError('non-digit found in ABN')
    if obj.startswith('0'):
        raise ValueError('leading zero not allowed in ABNs')
    digits = [int(c) for c in obj]
    digits[0] -= 1
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    assert len(digits) == len(weights) == 11
    chksum = sum(d*w for d,w in zip(digits, weights)) % 89
    return chksum == 0

def isacn(obj):
    """isacn(string or int) -> True|False

    Validate an ACN (Australian Company Number).
    http://www.asic.gov.au/asic/asic.nsf/byheadline/Australian+Company+Number+(ACN)+Check+Digit

    Accepts an int, or a string of digits including any leading zeroes.
    Digits may be optionally separated with spaces. Any other input raises
    TypeError or ValueError.

    Return True if the argument is a valid ACN, otherwise False.

    >>> isacn('004 085 616')
    True
    >>> isacn('005 085 616')
    False

    """
    if isinstance(obj, int):
        if not 0 <= obj < 10**9:
            raise ValueError('int out of range for an ACN')
        obj = '%09d' % obj
        assert len(obj) == 9
    if not isinstance(obj, str):
        raise TypeError('expected a str or int but got %s' % type(obj))
    obj = obj.replace(' ', '')
    if len(obj) != 9:
        raise ValueError('ACN must have exactly 9 digits')
    if not obj.isdigit():
        raise ValueError('non-digit found in ACN')
    digits = [int(c) for c in obj]
    weights = [8, 7, 6, 5, 4, 3, 2, 1]
    assert len(digits) == 9 and len(weights) == 8
    chksum = 10 - sum(d*w for d,w in zip(digits, weights)) % 10
    if chksum == 10:
        chksum = 0
    return chksum == digits[-1]


if __name__ == '__main__':
    # Check the list of valid ACNs from the ASIC website.
    ACNs = '''
        000 000 019  *  000 250 000  *  000 500 005  *  000 750 005
        001 000 004  *  001 250 004  *  001 500 009  *  001 749 999
        001 999 999  *  002 249 998  *  002 499 998  *  002 749 993
        002 999 993  *  003 249 992  *  003 499 992  *  003 749 988
        003 999 988  *  004 249 987  *  004 499 987  *  004 749 982
        004 999 982  *  005 249 981  *  005 499 981  *  005 749 986
        005 999 977  *  006 249 976  *  006 499 976  *  006 749 980
        006 999 980  *  007 249 989  *  007 499 989  *  007 749 975
        007 999 975  *  008 249 974  *  008 499 974  *  008 749 979
        008 999 979  *  009 249 969  *  009 499 969  *  009 749 964
        009 999 964  *  010 249 966  *  010 499 966  *  010 749 961
        '''.replace('*', '\n').split('\n')
    ACNs = [s for s in ACNs if s and not s.isspace()]
    for s in ACNs:
        n = int(s.replace(' ', ''))
        if not (isacn(s) and isacn(n) and not isacn(n+1)):
            print('test failed for ACN:  %s' % s.strip())
            break
    else:
        print('all ACNs tested okay')

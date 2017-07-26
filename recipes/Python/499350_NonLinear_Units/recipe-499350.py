class DB:
    '''
    Convience class for decibel scale.  Other non-linear scales such as the richter scale could be handled similarly.
    Usage:
    dB = DB()
    .
    . (later)
    .
    gain = 15 * dB

    '''
    def __rmul__(self, val):
        '''
        Only allow multiplication from the right to avoid confusing situation
        like: 15 * dB * 10
        '''
        return 10 ** (val / 10.)

def __test__():
    dB = DB()

    gain = 10 * dB
    assert abs(gain - 10) < 1e-8

    try:    
        gain2 = dB * 10
        raise Exception('Should raise a type error!')
    except TypeError:
        pass

__test__()

def binary_prefix(value, binary=True):
    '''Return a tuple with a scaled down version of value and it's binary prefix
                                        
    Parameters:                       
    - `value`: numeric type to trim down
    - `binary`: use binary (ICE) or decimal (SI) prefix
    '''       
    SI = 'kMGTPEZY'   
    unit = binary and 1024. or 1000.
    for i in range(-1, len(SI)):
        if abs(value) < unit:
            break
        value/= unit
    return (value, i<0 and '' or (binary and SI[i].upper() + 'i' or SI[i]))

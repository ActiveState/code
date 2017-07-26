import sys, struct, ctypes

def set_float(obj, value):
    assert isinstance(obj, float), 'Object must be a float!'
    assert isinstance(value, float), 'Value must be a float!'
    stop = sys.getsizeof(obj)
    start = stop - struct.calcsize('d')
    array = ctypes.cast(id(obj), ctypes.POINTER(ctypes.c_ubyte))
    for args in zip(range(start, stop), struct.pack('d', value)):
        array.__setitem__(*args)

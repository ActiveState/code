import inspect,dis

def expecting():
    """Return how many values the caller is expecting"""
    f = inspect.currentframe()
    f = f.f_back.f_back
    c = f.f_code
    i = f.f_lasti
    bytecode = c.co_code
    instruction = ord(bytecode[i+3])
    if instruction == dis.opmap['UNPACK_SEQUENCE']:
        howmany = ord(bytecode[i+4])
        return howmany
    elif instruction == dis.opmap['POP_TOP']:
        return 0
    return 1

def cleverfunc():
    howmany = expecting()
    if howmany == 0:
        print "return value discarded"
    if howmany == 2:
        return 1,2
    elif howmany == 3:
        return 1,2,3
    return 1

def test():
    cleverfunc()
    x = cleverfunc()
    print x
    x,y = cleverfunc()
    print x,y
    x,y,z = cleverfunc()
    print x,y,z

test()

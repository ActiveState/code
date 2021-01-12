import sys
import dis

def expecting():
    """Return how many values the caller is expecting"""
    f = sys._getframe(-1)
    f = f.f_back.f_back
    c = f.f_code
    i = f.f_lasti + 2
    if sys.version_info.major<3:
        i += 1
    bytecode = c.co_code.decode("latin-1")
    instruction = ord(bytecode[i])
    if instruction == dis.opmap['UNPACK_SEQUENCE']:
        howmany = ord(bytecode[i+1])
        return howmany
    elif instruction == dis.opmap['POP_TOP']:
        return 0
    return 1

if __name__ == '__main__':
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
        print(x)
        x,y = cleverfunc()
        print(x,y)
        x,y,z = cleverfunc()
        print(x,y,z)

    test()

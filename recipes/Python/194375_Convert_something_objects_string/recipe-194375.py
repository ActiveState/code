import marshal
import pickle
import urllib

class ArgumentConverter:
    "Convert a argument to one of some object"

    def str_convert(self, arg):
        return arg

    def int_convert(self, arg):
        try: return int(arg)
        except: pass
        return long(arg)
    
    def long_convert(self, arg):
        return long(arg)

    def float_convert(self, arg):
        return float(arg)

    def list_convert(self, arg):
        vals = []
        for token in arg.split(','):
            vals.append(self.convert(token))
        return vals

    def tuple_convert(self, arg):
        return tuple(self.list_convert(arg))

    def file_convert(self, arg):
        return open(arg)

    def marshal_convert(self, arg):
        return marshal.load(open(arg))

    def pickle_convert(self, arg):
        return pickle.load(open(arg))

    def uri_convert(self, arg):
        return urllib.urlopen(arg)

    s_convert = str_convert
    i_convert = int_convert
    l_convert = long_convert
    f_convert = float_convert
    L_convert = list_convert    
    T_convert = tuple_convert    
    F_convert = file_convert    
    M_convert = marshal_convert    
    P_convert = pickle_convert        
    U_convert = uri_convert    

    def convert(self, arg):
        suffix = 'str' # default suffix
        if arg.count(':'):
            suffix, value = arg.split(':', 1)
        else:
            value = arg
        return apply(getattr(self, suffix + '_convert'), (value,))

import sys

def getusage():
    return '''\
    str(s):string    String(default)
    int(i):int       Integer(convert to Long type, if it value is too long)
    long(l):long     Long
    float(f):float   Float
    file(F):file     File object
    marshal(M):file  Marshalized file object
    pickle(P):file   Pickled file object
    uri(U):uri       Opened uri file object
    list(L):list     List('list:int:1,file:foo' is [1, <file foo>])
    tuple(T):tuple   Tuple('tuple:int:1,file:foo' is (1, <file foo>))'''

def usage():
    print >>sys.stderr, 'Argument synopsis'
    print >>sys.stderr, getusage()

def test():
    aconv = ArgumentConverter()    
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    for arg in sys.argv[1:]:
        print aconv.convert(arg)

if __name__ == '__main__':
    test()

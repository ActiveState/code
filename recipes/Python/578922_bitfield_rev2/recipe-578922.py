#
# bitfield manipulation
#

class bf(object):
    def __init__(self,value=0):
        "Init bitfield with a value int in bin, hex, oct or dec"
        self._d = value

    def __getitem__(self, index):
        "return bit value for that index (n-0)"
        return (self._d >> index) & 1 

    def __setitem__(self,index,value):
        "set bit value for that index (n-0)"
        value    = (value&1)<<index
        mask     = (1)<<index
        self._d  = (self._d & ~mask) | value

    def __getslice__(self, start, end):
        "return bits slice from start to end (n-0)"
        mask = 2**(end - start + 1) -1
        return ((self._d >> start) & mask)

    def __setslice__(self, start, end, value):
        "set bits slice from start to end index (n-0) with the given value"
        mask = 2**(end - start + 1) -1
        value = (value & mask) << start
        mask = mask << start
        self._d = (self._d & ~mask) | value
        return (self._d >> start) & mask

    def __int__(self):
        "add de int() function for bf"
        return self._d
    
    def int(self):
        "add the bf.int() function return int"
        return self._d

    def bin(self):
        "add the bf.bin() function return str"
        return '{0:0b}'.format(self._d)
    
    def hex(self):
        "add the bf.hex() function return str"
        return '{0:0x}'.format(self._d)
        
    def __repr__(self):
        "add the basic return function, return bin str"
        return '{0:0b}'.format(self._d)
    
    def __len__(self):
        "add the len() function return int with the bit number count"
        return len('{0:0b}'.format(self._d))

    def unpack(self,pack):
        "return the unpack bit fields in dec [ n1, n2, n3...] with length given in pack [ l1, l2, l3...]"
        r=[]; ss=0;pack.reverse()      
        for i in pack:
            r.append(self.__getslice__(ss,ss+i-1))
            ss +=i
        r.reverse()
        return  r

    def pack(self,pack):
        "return bf with the given values in dec [n1, n2, n3...] packed"
        r=bf(); ss=0;pack.reverse()      
        for i in pack:
            l1=len(bin(i))-2
            r.__setslice__(ss,ss+l1,i)
            ss +=l1
        return  r    


if __name__ == "__main__":

    k = bf(0x0f)
    k[10:20] =0xfffffffffff
    k[3:7]=0b10101
    print k[3]
    print k[5]
    
    print k
    print len(k)
    
    print k.unpack([5, 3,1,7]),(k.unpack([5, 3,1,7]))[1]
    b1,b2,b3,b4 =  k.unpack([5, 3,1,7])
    print b1,b2,b3,b4
    
    print bf().pack([0b1101,0b1001])

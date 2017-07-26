def isOdd(integer):
    #assert isinstance(integer, int)
    return integer % 2 == 1

def isEven(integer):
    #assert isinstance(integer, int)
    return integer % 2 == 0

def _list_to_string(li):
    return ''.join(map(str, li))

class GrayCode(object):
    def __init__(self, nbits):
        self._nbits = nbits
        self._grayCode = []
        self.__generate()

    def __getitem__(self, i):
        return self._grayCode[i]

    def __str__(self):
        return str(self._grayCode)

    __repr__ = __str__

    def __iter__(self):            
        return self._grayCode.__iter__()

    def __generate(self):
        li = [0 for i in xrange(self._nbits)]
        self._grayCode.append(_list_to_string(li))

        for term in xrange(2, (1<<self._nbits)+1):
            if isOdd(term):                
                for i in xrange(-1,-(self._nbits),-1):
                    if li[i]==1:                        
                        li[i-1]=li[i-1]^1                        
                        break
                    
            if isEven(term):
                li[-1]=li[-1]^1

            self._grayCode.append(_list_to_string(li))

class GrayCodeIterator(object):
    def __init__(self, nbits):
        self._nbits = nbits

    def __iter__(self):
        li = [0 for i in xrange(self._nbits)]
        yield _list_to_string(li)

        for term in xrange(2, (1<<self._nbits)+1):
            if isOdd(term):                
                for i in xrange(-1,-(self._nbits),-1):
                    if li[i]==1:                        
                        li[i-1]=li[i-1]^1                        
                        break
                    
            if isEven(term):
                li[-1]=li[-1]^1

            yield _list_to_string(li)


if __name__=='__main__':
    d = 4
    codes=GrayCode(d)
    print '%d digits gray codes:' % d
    print codes
    print 'Using Iterator:'
    #for c in GrayCode(20):  
    #    print c
    for c in GrayCodeIterator(20):
        print c

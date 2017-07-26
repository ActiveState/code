''' Bit Array - Bit array computing with long integers.
Good for around 1,000,000 bit arrays but gets slow with a billion bits...
Mike Sweeney. June 2013.

Positives:
Works even with old versions of Python.
Only pure Python needed - no third party modules.
Binary operations such as & | ^ << and >> are fast.
Store and load are fast and compact.

Negatives:
Longs are passed by value so no in-place operations are possible.
Array changing operations are slow on large arrays.

Timing of one AND operation on bit arrays with Python 2.7 on AMD 3.8 GHz 4 core:
1,000,000 bit         15 us
10,000,000 bit       320 us
100,000,000 bit      6.2 ms
1,000,000,000 bit     86 ms    (125MB bit array objects)
'''

# Constructors for bit arrays:
bitarray = long
def frombin(s): return int(s, 2)

# Operations on bit arrays of the same size:
def issubset(a, b): return a & b == a
def subtract(a, b): return a & ~b
# use & | ^ and ~ for other bitarray operations

# Change a bit value in a bit array:
def setbit(a, n): return a | (1<<n)
def unsetbit(a, n): return a & ~(1<<n)
def toggle(a, n): return a ^ (1<<n)

# Append and pop will add or remove a bit from the end of the array:
def append(a, v): return (a<<1) | v
def pop(a):
    v = (a & 1)
    new_a = (a >> 1)
    return new_a, v

# Query a bitarray:
def getbit(a, n): return a & (1<<n)
def countbits(a): return bin(a).count('1')
def activebits(a):
    s=bin(a)[2:][::-1]
    return [i for i,d in enumerate(s) if d == '1']
def tostring(a, w=0): return bin(a)[2:].zfill(w)

# Convert bit arrays for storage in files or databases:
import cPickle
def store(a): return cPickle.dumps(a, -1)
def load(data): return cPickle.loads(data)


def _analyticsdemo():
    USERS = 1000000
    from random import randint

    def randarray(n,arr=0):
        for i in xrange(n):
            arr = setbit(arr, randint(0, USERS-1))
        return arr

    admin = randarray(1000)
    upload24hr = randarray(1000)
    badpwd7days = randarray(10000)
    member2012 = randarray(100000)

    maybehacker = badpwd7days & upload24hr & ~admin & ~member2012
    print 'Possible hacker users:', activebits(maybehacker)

if __name__ == '__main__':
    _analyticsdemo()

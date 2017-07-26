import array, random

TEADELTA     = 0x9e3779b9L
TEAROUNDS    = 32
TEASBOXSIZE  = 128
TEASBOXSHIFT = 7

class randrange(object):
    def __init__(self, start, stop):
        self.start = start
        self.max = stop - start
        self.sbox = array.array('I', [ random.randint(0, 0xffffffffL)
                                       for i in range(TEASBOXSIZE) ])
        bits = 0
        while (1 << bits) < self.max:
            bits += 1
        self.left = bits / 2
        self.right = bits - self.left
        self.mask = (1 << bits) - 1

        if TEASBOXSIZE < (1 << self.left):
            self.sboxmask = TEASBOXSIZE - 1
            self.kshift = TEASBOXSHIFT
        else:
            self.sboxmask = (1 << self.left) - 1
            self.kshift = self.left

    def __iter__(self):
        enc = 0
        for i in range(self.max):
            c = self.max
            while c >= self.max:
                c = enc
                enc += 1
                s = 0
                for j in range(TEAROUNDS):
                    s += TEADELTA
                    c ^= (self.sbox[(c ^ s) & self.sboxmask] << self.kshift)
                    c = (c + s) & self.mask
                    c = ((c << self.left) | (c >> self.right)) & self.mask
            yield self.start + c

    def __len__(self):
        return self.max

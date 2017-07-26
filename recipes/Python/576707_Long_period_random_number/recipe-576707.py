import random

class CMWC(random.Random):
    'Long period random number generator: Complementary Multiply with Carry'
    # http://en.wikipedia.org/wiki/Multiply-with-carry

    a = 3636507990
    logb = 32
    b = 2 ** logb
    r = 1359

    def _gen_word(self):
        i = self.i
        xc, self.c = divmod(self.a * self.Q[i] + self.c, self.b)
        x = self.Q[i] = self.b - 1 - xc
        self.i = 0 if i + 1 == self.r else i + 1
        return x

    def getrandbits(self, k):
        while self.bits < k:
            self.f = (self.f << self.logb) | self._gen_word()
            self.bits += self.logb
        x = self.f & ((1 << k) - 1)
        self.f >>= k;  self.bits -= k
        return x

    def random(self, RECIP_BPF=random.RECIP_BPF, BPF=random.BPF):
        return self.getrandbits(BPF) * RECIP_BPF

    def seed(self, seed=None):
        seeder = random.Random(seed)
        Q = [seeder.randrange(0x100000000) for i in range(self.r)]
        c = seeder.randrange(0x100000000)
        self.setstate((0, 0, 0, c, Q))

    def getstate(self):
        return self.f, self.bits, self.i, self.c, tuple(self.Q)

    def setstate(self, (f, bits, i, c, Q)):
        self.f, self.bits, self.i, self.c, self.Q = f, bits, i, c, list(Q)


if __name__ == '__main__':
    prng = CMWC(134123413541344)
    for i in range(20):
        print prng.random()
    print
    for i in range(20):
        print normalvariate(mu=5.0, sigma=2.2)

# This piece of code is more mathy than normal; it shows that there's a
# correspondance between the positive integers and the positive fractions.
# For example:

###
# >>> two2one(0,0)
# 0
# >>> two2one(1,0)
# 1
# >>> two2one(3,4)
# 32
# >>> one2two(31)
# (4, 3)
# >>> one2two(32)
# (3, 4)
###

# and it's related to the math proof that the rationals are countable.

# It can also be used to take the "cross-product" of two infinite sequences,
# so it's not quite "useless", but it is weird.  *grin*  Hope you like it.


###
def two2one(x, y):
    """Maps a positive (x,y) to an element in the naturals."""
    diag = x + y
    bottom = diag * (diag + 1) / 2
    return bottom + y

def one2two(k):
    """Inverts the two2one map --- given a natural number, return its
    corresponding (x,y) pair."""
    diag = int((sqrt(1 + 8*k) - 1) / 2)
    offset = k - diag * (diag + 1) / 2
    return (diag - offset, offset)


class xcross_inf:
    def __init__(self, X, Y):
        self.X, self.Y = X, Y
    def __getitem__(self, key):
        i, j = one2two(key)
        return (self.X[i], self.Y[j])

class Evens:
    def __getitem__(self, key):
        return key * 2

class Odds:
    def __getitem__(self, key):
        return key * 2 + 1

def test2():
    seq = xcross_inf(Evens(), Odds())
    for i in range(20): print seq[i]
###

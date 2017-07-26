#  A very slow arithmetic coder for Python.
#
#  "Rationals explode quickly in term of space and ... time."
#              -- comment in Rational.py (probably Tim Peters)
#
# Really.  Don't use this for real work.  Read Mark Nelson's
# Dr. Dobb's article on the topic at
#    http://dogma.net/markn/articles/arith/part1.htm
# It's readable, informative and even includes clean sample code.
#
# Contributed to the public domain
# Andrew Dalke < dalke @ dalke scientific . com >


import sys

import Rational, math
R = Rational.rational

def train(text):
    """text -> 0-order probability statistics as a dictionary

    Text must not contain the NUL (0x00) character because that's
    used to indicate the end of data.
    """
    assert "\x00" not in text
    counts = {}
    for c in text:
        counts[c]=counts.get(c,0)+1
    counts["\x00"] = 1
    tot_letters = sum(counts.values())

    tot = 0
    d = {}
    prev = R(0)
    for c, count in counts.items():
        next = R(tot + count, tot_letters)
        d[c] = (prev, next)
        prev = next
        tot = tot + count
    assert tot == tot_letters

    return d


def encode(text, probs):
    """text and the 0-order probability statistics -> longval, nbits

    The encoded number is rational(longval, 2**nbits)
    """
    minval = R(0)
    maxval = R(1)
    for c in text + "\x00":
        prob_range = probs[c]
        delta = maxval - minval
        maxval = minval + prob_range[1] * delta
        minval = minval + prob_range[0] * delta

    # I tried without the /2 just to check.  Doesn't work.
    # Keep scaling up until the error range is >= 1.  That
    # gives me the minimum number of bits needed to resolve
    # down to the end-of-data character.
    delta = (maxval - minval)/2
    nbits = 0L
    while delta < 1:
        nbits = nbits + 1
        delta = delta << 1
    if nbits == 0:
        return 0, 0
    else:
        avg = (maxval + minval)<<(nbits-1)  # using -1 instead of /2
    # Could return a rational instead ...
    return avg.n//avg.d, nbits  # the division truncation is deliberate


def decode(longval, nbits, probs):
    """decode the number to a string using the given statistics"""
    val = R(longval, 1L<<nbits)
    letters = []
    probs_items = [(c, minval, maxval) for (c, (minval, maxval))
                                 in probs.items()]

    while 1:
        for (c, minval, maxval) in probs_items:
            if minval <= val < maxval:
                break
        else:
            raise AssertionError("not found")

        if c == "\x00":
            break
        letters.append(c)
        delta = maxval - minval
        val = (val - minval)/delta
    return "".join(letters)

if __name__ == "__main__":
    # getopt? optparse? What are they?
    import sys
    trainfilename = sys.argv[1]  # must give a filename
    phrase = sys.argv[2]  # must give text to compress (slowly!)
    probs = train(open(trainfilename).read())
    n, nbits = encode(phrase, probs)
    # +1 for the NUL terminator or equivalent
    print "Orig. %d bits, compr. %d bits, ratio = %3.f%%" % (
        (len(phrase)+1)*8, nbits, (100.*nbits) / (len(phrase)*8+1))
    print n
    new_phrase = decode(n, nbits, probs)
    print "Was it '%s'?" % (new_phrase,)
    if phrase == new_phrase:
        print "Guess so."
    else:
        print "Why not?!"

#!/usr/bin/env python
""" Walker's alias method for random objects with different probablities
    walkerrandom.py

Examples
--------

    # 0 1 2 or 3 with probabilities .1 .2 .3 .4 --
  wrand = Walkerrandom( [10, 20, 30 40] )  # builds the Walker tables
  wrand.random()  # each call -> 0 1 2 or 3
    # for example, 1000 calls with random.seed(1) -> [96, 199, 334, 371]

    # strings A B C or D with probabilities .1 .2 .3 .4 --
  abcd = dict( A=1, D=4, C=3, B=2 )
    # keys can be any immutables: 2d points, colors, atoms ...
  wrand = Walkerrandom( abcd.values(), abcd.keys() )
  wrand.random()  # each call -> "A" "B" "C" or "D"
                  # fast: 1 randint(), 1 uniform(), table lookup

How it works
------------

For weights 10 20 30 40 as above, picture sticks A B C D of those lengths:

    10  AAAAAAAAAA
    20  BBBBBBBBBB BBBBBBBBBB
    30  CCCCCCCCCC CCCCCCCCCC CCCCCCCCCC
    40  DDDDDDDDDD DDDDDDDDDD DDDDDDDDDD DDDDDDDDDD

Split and rearrange them into equal-length rows, like this:

    AAAAAAAAAA DDDDDDDDDDDDDDD  -- 10 A + 15 D = 40% A + 60% D
    BBBBBBBBBBBBBBBBBBBB DDDDD  -- 20 B + 5 D  = 80% B + 20% D
    CCCCCCCCCCCCCCCCCCCCCCCCC   -- 25 C        = 100% C
    DDDDDDDDDDDDDDDDDDDD CCCCC  -- 20 D + 5 C  = 80% D + 20% C

Clearly 10 % of the area is A, 20 % B, 30 % C and 40 % D --
we haven't changed areas, just rearranged.
Now to choose a random one of A or B or C or D,
throw a dart at a "dart board" of the sticks in these 4 rows:
if it hits row 0, return A with probablity 40 % / D 60 %
if it hits row 1, return B with probablity 80 % / D 20 %
...
This picture is in Devroye, p. 111 (rediscovered here).

Walker's algorithm essentially arranges a given lot of sticks
into equal-length rows: pick a row shorter than average
and a row longer than average, split the longer to fill the shorter,
iterate until they're all the same length.


Notes

  To generate random colors similar to those in a given picture,
  first collect color samples in a histogram:
    for color in ...:
        # cluster e.g. rrggbb -> rgb, 16^3 bins
        # (many many methods, see Wikipedia Data_clustering)
        colors[color] += 1
    (cPickle to a file, write it, read it back in)
  then use Walkerrandom to select colors with these frequencies:
      colorrand = Walkerrandom( colors.values(), colors.keys() )
      colorrand.random()  # each call -> a color

References

    L. Devroye, Non-Uniform Random Variate Generation, 1986, p. 107 ff.
        http://cg.scs.carleton.ca/~luc/rnbookindex.html (800 pages)
    Knuth, Stanford GraphBase, 1993, p. 392
    C++ hat random container by AngleWyrm,
        http://home.comcast.net/~anglewyrm/hat.html

"""

from __future__ import division
import random

__author__ = "Denis Bzowy"
__version__ = "16nov2008"
Test = 0

#...............................................................................
class Walkerrandom:
  """ Walker's alias method for random objects with different probablities
  """

  def __init__( self, weights, keys=None ):
    """ builds the Walker tables prob and inx for calls to random().
        The weights (a list or tuple or iterable) can be in any order;
        they need not sum to 1.
    """
    n = self.n = len(weights)
    self.keys = keys
    sumw = sum(weights)
    prob = [w * n / sumw for w in weights]  # av 1
    inx = [-1] * n
    short = [j for j, p in enumerate( prob ) if p < 1]
    long = [j for j, p in enumerate( prob ) if p > 1]
    while short and long:
        j = short.pop()
        k = long[-1]
        # assert prob[j] <= 1 <= prob[k]
        inx[j] = k
        prob[k] -= (1 - prob[j])  # -= residual weight
        if prob[k] < 1:
            short.append( k )
            long.pop()
        if Test:
            print "test Walkerrandom: j k pk: %d %d %.2g" % (j, k, prob[k])
    self.prob = prob
    self.inx = inx
    if Test:
        print "test", self

  def __str__( self ):
    """ e.g. "Walkerrandom prob: 0.4 0.8 1 0.8  inx: 3 3 -1 2" """
    probstr = " ".join([ "%.2g" % x for x in self.prob ])
    inxstr = " ".join([ "%.2g" % x for x in self.inx ])
    return "Walkerrandom prob: %s  inx: %s" % (probstr, inxstr)

#...............................................................................
  def random( self ):
    """ each call -> a random int or key with the given probability
        fast: 1 randint(), 1 random.uniform(), table lookup
    """
    u = random.uniform( 0, 1 )
    j = random.randint( 0, self.n - 1 )  # or low bits of u
    randint = j if u <= self.prob[j] \
        else self.inx[j]
    return self.keys[randint] if self.keys \
        else randint


#...............................................................................
if __name__ == "__main__":
    # little examples, self-contained --
    N = 5
    Nrand = 1000
    randomseed = 1
    try:
        import bz.util
        bz.util.scan_eq_args( globals(), __doc__ )  # N=5 ...
    except ImportError:
        pass
    if randomseed:
        random.seed( randomseed )

    print Nrand, "Walkerrandom with weights .1 .2 .3 .4:"
    w = range( 1, N )
    wrand = Walkerrandom( w )
    nrand = [0] * (N - 1)
    for _ in range( Nrand ):
        j = wrand.random()
        nrand[j] += 1
    s = str( nrand )
    print s
    if N==5 and Nrand==1000 and randomseed==1:
        assert s == "[96, 199, 334, 371]"

    print Nrand, "Walkerrandom strings with weights .1 .2 .3 .4:"
    abcd = dict( A=1, D=4, C=3, B=2 )
    wrand = Walkerrandom( abcd.values(), abcd.keys() )
    from collections import defaultdict
    nrand = defaultdict(int)  # init 0
    for _ in range( Nrand ):
        j = wrand.random()
        nrand[j] += 1
    s = str( sorted( nrand.iteritems() ))
    print s
    if N==5 and Nrand==1000 and randomseed==1:
        assert s == "[('A', 105), ('B', 181), ('C', 283), ('D', 431)]"

# end walkerrandom.py

"""
wchoice.py -- by bearophile, V.1.0 Oct 30 2006

Weighted choice: like the random.choice() when the probabilities of
the single elements aren't the same.
"""

from random import random
from bisect import bisect
from itertools import izip

def wchoice(objects, frequences, filter=True, normalize=True):
    """wchoice(objects, frequences, filter=True, normalize=True): return
    a function that return the given objects with the specified frequency
    distribution. If no objects with frequency>0 are given, return a
    constant function that return None.

    Input:
      objects: sequence of elements to choose.
      frequences: sequence of their frequences.
      filter=False disables the filtering, speeding up the object creation,
        but less bad cases are controlled. Frequences must be float > 0.
      normalize=False disables the probablitity normalization. The choice
        becomes faster, but sum(frequences) must be 1
    """
    if filter:
        # Test and clean the frequencies.
        if isinstance(frequences, (set, dict)):
            raise "in wchoice: frequences: only ordered sequences."
        if isinstance(objects, (set, dict)):
            raise "in wchoice: objects: only ordered sequences."
        if len(frequences) != len(objects):
            raise "in wchoice: objects and frequences must have the same lenght."
        frequences = map(float, frequences)
        filteredFreq = []
        filteredObj = []
        for freq, obj in izip(frequences, objects):
            if freq < 0:
                raise "in wchoice: only positive frequences."
            elif freq >1e-8:
                filteredFreq.append(freq)
                filteredObj.append(obj)

        if len(filteredFreq) == 0:
            return lambda: None
        if len(filteredFreq) == 1:
            return lambda: filteredObj[0]
        frequences = filteredFreq
        objects = filteredObj
    else:
        if len(objects) == 1:
            return lambda: objects[0]
        # Here objects is unaltered, so it must have a fast __getitem__

    addedFreq = []
    lastSum = 0
    for freq in frequences:
        lastSum += freq
        addedFreq.append(lastSum)

    # If the choice method is called many times, then the frequences
    # can be normalized to sum 1, so instead of random()*self.sumFreq
    # a random() suffices.
    if normalize:
        return lambda rnd=random, bis=bisect: objects[bis(addedFreq, rnd()*lastSum)]
    else:
        return lambda rnd=random, bis=bisect: objects[bis(addedFreq, rnd())]


if __name__ == '__main__':
    print "wchoice tests:"
    objs = "ABCDE"
    freqs = [1, 3, 1.1, 0, 5]
    sumf = sum(freqs)
    wc = wchoice(objs, freqs)
    freq1 = dict.fromkeys(objs, 0)
    nestractions = 100000
    for i in xrange(nestractions):
        freq1[wc()] += 1

    freq2 = sorted(freq1.items())
    freq3 = [sumf*float(v)/nestractions for (k,v) in freq2]

    for (f1,f2) in zip(freq3, freqs):
        print abs(f1-f2),
        assert abs(f1-f2) < 0.05
    print "\n"

    wc = wchoice(["a"], [1])
    assert set(wc() for i in xrange(20000)) == set(["a"])

    wc = wchoice(["a"], [0])
    assert set(wc() for i in xrange(20000)) == set([None])

    wc = wchoice(["a","b"], [0,0])
    assert set(wc() for i in xrange(20000)) == set([None])

    objs = ["A"]
    freqs = [1.5]
    wc = wchoice(objs, freqs, filter=False)
    assert [wc() for _ in xrange(10)] == ["A"] * 10

    objs = "ABCDE"
    freqs = [1, 3, 1.1, 0.1, 5]
    wc = wchoice(objs, freqs, filter=False)
    print [wc() for _ in xrange(50)]

    print "Tests done."

import bisect
import random
import unittest

try:
    xrange
except NameError:
    # Python 3.x
    xrange = range


def weighted_random_choice(seq, weight):
    """Returns a random element from ``seq``. The probability for each element
    ``elem`` in ``seq`` to be selected is weighted by ``weight(elem)``.

    ``seq`` must be an iterable containing more than one element.

    ``weight`` must be a callable accepting one argument, and returning a
    non-negative number. If ``weight(elem)`` is zero, ``elem`` will not be
    considered. 
        
    """ 
    weights = 0
    elems = [] 
    for elem in seq:
        w = weight(elem)     
        try:
            is_neg = w < 0
        except TypeError:    
            raise ValueError("Weight of element '%s' is not a number (%s)" %
                             (elem, w))
        if is_neg:
            raise ValueError("Weight of element '%s' is negative (%s)" %
                             (elem, w))
        if w != 0:               
            try:
                weights += w
            except TypeError:
                raise ValueError("Weight of element '%s' is not a number "
                                 "(%s)" % (elem, w))
            elems.append((weights, elem))
    if not elems:
        raise ValueError("Empty sequence")
    ix = bisect.bisect(elems, (random.uniform(0, weights), None))
    return elems[ix][1]
        

class TestCase(unittest.TestCase):

    def test_empty(self):
        """Empty sequences raise ``ValueError``.

        """
        self.assertRaises(ValueError,
                          weighted_random_choice, [], lambda x: 0)
        self.assertRaises(ValueError,
                          weighted_random_choice, [1, 2, 3], lambda x: 0)

    def test_invalid_weight(self):
        """Invalid weight values are detected.

        """
        self.assertRaises(ValueError,
                          weighted_random_choice, [1, 2, 3], lambda x: "foo")

        class Oops(Exception):
            pass

        def weight(elem):
            raise Oops()

        self.assertRaises(Oops, weighted_random_choice, [1, 2, 3], weight)

    def test_spread(self):
        """Results are consistent with weight function.

        """
        seq = range(0, 100)
        odds, evens = [], []

        bias = 10.0

        def weight(elem):
            if elem % 2:
                return bias
            else:
                return 1

        for _ in xrange(0, 5000):
            elem = weighted_random_choice(seq, weight)
            if elem % 2:
                odds.append(elem)
            else:
                evens.append(elem)

        delta = abs(bias - float(len(odds) / float(len(evens))))
        self.assertTrue(delta < 1)


if __name__ == "__main__":
    random.seed()
    unittest.main()

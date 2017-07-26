#! /usr/bin/env python

from __future__ import generators
import unittest

def repeating_alternator(*args):
    """Return a repeating alternator for args."""
    while args:
        for a in args:
            yield a

def finite_alternator(length, *args):
    """Return a finite repeating alternator for args."""
    c = 0
    while args and c < length:
        for a in args:
            yield a
            c += 1
            if c >= length:
                break

def finite_iterator(n, iterator):
    """Return an iterator that will stop after generating n elements."""
    for j in xrange(n):
        yield iterator.next()

def weave_sets(set_n, set_m):
    """Return an iterator for set_n and set_m that stops when set_n is
    exhausted.  If set_n is larger than set_m, cycle over set_m.
    """
    m = len(set_m)
    if not m:
        raise ValueError("Set to be cycled on cannot be empty.")
    for i in range(len(set_n)):
        yield set_n[i], set_m[i%m]
    # In Python 2.3, this can be simplified to:
    #for index, item in enumerate(set_n):
    #    yield item, set_m[index%m]

def weave_items(iterator, alternator, weave_item):
    """Return an iterator for iterator, applying weave_item to each item with
    its pair in alternator.
    """
    for item in iterator:
        yield weave_item(item, alternator.next())

def color_item(item, color):
    template = "<%(color)s>%(item)s</%(color)s>"
    return template % locals()

class test(unittest.TestCase):

    def setUp(self):
        self.colors = ("red", "orange", "yellow", "green", "blue", "indigo",
                       "violet")
        self.expected = ['<red>0</red>',
                         '<orange>1</orange>',
                         '<yellow>2</yellow>',
                         '<green>3</green>',
                         '<blue>4</blue>',
                         '<indigo>5</indigo>',
                         '<violet>6</violet>',
                         '<red>7</red>',
                         '<orange>8</orange>',
                         '<yellow>9</yellow>']
        self.length = 10

    def test_weave_sets(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        generated = [color_item(x, y) for x, y in weave_sets(range(length), colors)]
        self.assertEquals(expected, generated)

    def test_zip(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        iterator = range(length)
        alternator = repeating_alternator(*colors)
        weaved = zip(iterator, alternator)
        generated = [color_item(x, y) for x, y in weaved]
        self.assertEquals(expected, generated)

    def test_list_comprehension(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        iterator = range(length)
        alternator = repeating_alternator(*colors)
        generated = [color_item(x, alternator.next()) for x in iterator]
        self.assertEquals(expected, generated)

    def test_map_finite_alternator(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        iterator = range(length)
        alternator = finite_alternator(length, *colors)
        generated = map(color_item, iterator, alternator)
        self.assertEquals(expected, generated)

    def test_map_finite_iterator(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        iterator = range(length)
        alternator = repeating_alternator(*colors)
        alternator = finite_iterator(length, alternator)
        generated = map(color_item, iterator, alternator)
        self.assertEquals(expected, generated)

    def test_weave_items(self):
        colors = self.colors
        length = self.length
        expected = self.expected

        iterator = range(length)
        alternator = repeating_alternator(*colors)
        generated = [x for x in weave_items(iterator, alternator, color_item)]
        self.assertEquals(expected, generated)

    def test_empty(self):
        r = repeating_alternator()
        self.assertRaises(StopIteration, r.next)

if __name__ == "__main__":
    unittest.main()

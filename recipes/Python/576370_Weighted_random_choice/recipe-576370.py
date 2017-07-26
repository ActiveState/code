#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from __future__ import division
import random, bisect
 
class ItemGenerator(object):
    '''Choices randomly an element from a list.

    It does it not uniformly, but using a given weight for
    each element.

    Just instantiate this class passing a list of pairs 
    (item, weight), and then call it to get the items.
    '''
    def __init__(self, items):
        self.puntos = []
        self.ponderado = []
        total = sum(x[1] for x in items)
        acum = 0
        for it,peso in items:
            acum += peso
            self.puntos.append(it)
            self.ponderado.append(acum/total)
        self.total = acum - 1

    def __call__(self):
        ind = random.random()
        cual = bisect.bisect(self.ponderado, ind)
        return self.puntos[cual]
 
if __name__ == "__main__":
    # This shows the usage, and also test the recipe, as calling that
    # a lot of times, it should return the elements in the same 
    # given proportion

    items = (
        ("A", 10),
        ("B", 100),
        ("C", 5)
    )

    itgen = ItemGenerator(items)
    cuenta = {}
    for i in range(1000000):
        item = itgen()
        cuenta[item] = cuenta.get(item, 0) + 1
    print cuenta

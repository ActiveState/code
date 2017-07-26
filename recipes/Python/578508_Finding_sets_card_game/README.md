## Finding sets in the card game SET!

Originally published: 2013-04-04 22:13:55
Last updated: 2013-04-05 12:49:36
Author: Sander Evers

In the card game [SET!](http://en.wikipedia.org/wiki/Set_%28game%29), players are shown an array of 12 (or more) symbol cards and try to identify a so-called 3-card **set** among these cards as quickly as possible.\n\nA card has four attributes (number, shape, color and shading), each of which can take 3 possible values. In a **set**, for each attribute, all three cards should have either the same value, or the three different values.\n\nThis recipe solves the problem of finding *all* sets within an array of an arbitrary number of cards, showing some clever optimizations and celebrating the clarity of Python in expressing the algorithms.
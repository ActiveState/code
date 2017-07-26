## Memoize Generator

Originally published: 2011-12-20 04:25:16
Last updated: 2012-01-02 05:53:19
Author: Peter Donis

A wrapper class for generators that "memoizes" them, so that even\nif the generator is realized multiple times, each term only gets\ncomputed once (after that the result is simply returned from a\ncache).\n
###guaranteed-stable sort with the decorate-sort-undecorate idiom (aka Schwartzian transform)

Originally published: 2001-03-15 07:18:43
Last updated: 2001-06-04 18:47:59
Author: Alex Martelli

Python lists' .sort method is not guaranteed stable -- items that compare equal may or may not be in unchanged order. Ensuring stability is easy as one of the many application of the commom idiom decorate-sort-undecorate (aka "Schwartzian transform").
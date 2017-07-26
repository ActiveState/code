###Generating combinations of objects from multiple sequences

Originally published: 2004-08-29 00:32:23
Last updated: 2004-08-29 00:32:23
Author: David Klaffenbach

The function combine takes multiple sequences and creates a list in which each item is constructed from items from each input sequence, and all possible combinations are created.  If that description is confusing, look at the example in the docstring.  It's a pretty simple transformation.  The function xcombine is similar, but returns a generator rather than creating the output all at once.
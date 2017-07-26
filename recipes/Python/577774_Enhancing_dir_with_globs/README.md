## Enhancing dir() with globs  
Originally published: 2011-07-01 04:03:45  
Last updated: 2011-07-01 04:03:46  
Author: Steven D'Aprano  
  
dir() is useful for interactively exploring the attributes and methods of objects at the command line. But sometimes dir() returns a lot of information:

    >>> len(dir(decimal.Decimal))  # too much information!
    137

It can be helpful to filter the list of names returned. This enhanced version of dir does exactly that, using simple string globbing:

    >>> dir(decimal.Decimal, '*log*')  # just attributes with "log" in the name
    ['_fill_logical', '_islogical', '_log10_exp_bound', 'log10', 'logb', 
    'logical_and', 'logical_invert', 'logical_or', 'logical_xor']


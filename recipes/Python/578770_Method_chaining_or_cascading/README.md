## Method chaining or cascading  
Originally published: 2013-11-22 11:13:24  
Last updated: 2016-09-01 12:34:17  
Author: Steven D'Aprano  
  
A frequently missed feature of built-ins like lists and dicts is the ability to chain method calls like this:

    x = []
    x.append(1).append(2).append(3).reverse().append(4)
    # x now equals [3, 2, 1, 4]

Unfortunately this doesn't work, as mutator methods return ``None`` rather than ``self``. One possibility is to design your class from the beginning with method chaining in mind, but what do you do with those like the built-ins which aren't?

This is sometimes called [method cascading](https://en.wikipedia.org/wiki/Method_cascading). Here's a proof-of-concept for an adapter class which turns any object into one with methods that can be chained.
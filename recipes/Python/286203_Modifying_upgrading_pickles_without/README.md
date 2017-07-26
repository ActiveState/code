###Modifying (upgrading) pickles without instantiating real app objects

Originally published: 2004-07-07 02:37:53
Last updated: 2004-07-07 12:22:32
Author: Christopher Armstrong

The following code loads arbitrary pickles (well, there are probably some that it won't load, like ones which have object states which aren't dicts). It just loads their data into totally inert objects which you can then traverse and do what you like to. It's pretty similar to processing a DOM tree.
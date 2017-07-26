###Dynamic Class Construction a la DSLs

Originally published: 2011-05-24 04:58:39
Last updated: 2011-08-13 04:00:46
Author: Eric Snow

So maybe it's not quite a mutable namedtuple.  However, I borrowed heavily against the namedtuple implementation for this one.\n\nI wanted to have a collection of classes that described data types without any functionality on them, sort of state holders.  However, I wanted to use defaults and I wanted it to be mutable.  \n\nI noticed, as I started building my classes, that each was following the same pattern, so I extracted it out into this recipe.  Wrapping namedtuple to get the same result would probably be feasible, but I enjoyed doing this too.\n\nThe distinction between parameters and properties is mostly one I was maintaining between single objects and collections.  Realistically everything could have been parameters.
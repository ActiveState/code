###Pickle Python Objects to a DOM tree and vice versa

Originally published: 2004-12-03 12:56:02
Last updated: 2004-12-04 01:35:32
Author: Uwe Schmitt

This receipe provides lightweight functions for pickling objects to a DOM structure and vice versa. I use it in connection with <a href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/286150">Hierarchical Objecs</a> from receipe #286150.\n\n<strong>This receipe makes use of eval(), so do not unpickle untrusted xml documents !!!</strong>. I add some secret checksums to my documents which I check before unpickling.
###Queue with tagged items

Originally published: 2009-01-26 06:55:58
Last updated: 2009-01-28 07:23:40
Author: Jirka Vejrazka

I needed multiple consumers to retrieve data from a queue fed by one producer. Could not find a good working code for that, so I implemented my own queue. Docstring should describe how this works.\n\nTwo notes:\n1) my code uses multiprocessing code, but in this module, the Lock and Condition could be easily replaced with the same objects from the threading module\n2) the attached test uses syntax for "nose" testing package, I did not convert it to doctest or UnitTest.\n
## Fast copy of an object having a slow __init__

Originally published: 2001-08-10 04:03:41
Last updated: 2001-08-10 04:03:41
Author: Alex Martelli

Special method __copy__ is the easiest way for an object to cooperate with the copy.copy function, but how do you bypass the object's __init__, if it's slow, to get an 'empty' object of this class?  Easy -- here's how.
## Generator for arbitrary assignment

Originally published: 2002-11-24 01:50:48
Last updated: 2002-11-24 01:50:48
Author: Brett Cannon

A discussion on python-dev ( http://mail.python.org/pipermail/python-dev/2002-November/030380.html ) came up with the idea of allowing arbitrary assignments::\n\n >>> a,b,*c = (1,2,3,4,5)\n >>> a\n 1\n >>> b\n 2\n >>> c\n (3, 4, 5)\n\nI didn't like the idea of adding this to the language for assignments, so I came up with a generator that basically does the above but assigns the last variable the used iterator, and all without any new syntax.\n\nThanks to Alex Martelli for simplifying the code and Oren Tirosh for coming up with better variable names.
## Yet another Python implementation of PEP 380 (yield from)

Originally published: 2010-03-26 19:46:29
Last updated: 2010-04-25 23:08:07
Author: Arnau Sanchez

Any Python programmer knows how extremely powerful [generators](http://www.python.org/dev/peps/pep-0255/) are. Now (since version 2.5) Python generators can not only yield values but also receive them, so they can be used to build [coroutines](http://www.python.org/dev/peps/pep-0342/).\n\nOne drawback of the current implementation of generators is that you can only yield/receive values to/from the immediate caller. That means, basically, that you cannot easily refactor your code and write nested generators. [PEP-380](http://www.python.org/dev/peps/pep-0380/) is the most serious effort to overcome this issue, but until it gets approved we can still play around with pure Python implementations of *yield from*. \n\nThis recipe follows terminology used by others in the past ([recipe566726](http://code.activestate.com/recipes/576727), [recipe576728](http://code.activestate.com/recipes/576728)), but I've tried to simplify  the code as much as possible.
###Concurrent Generator

Originally published: 2005-07-25 06:37:32
Last updated: 2005-07-25 06:37:32
Author: Calvin Spealman

This recipe is a simple pair of classes that implement something like what is proposed for <a href="http://www.python.org/peps/pep-0342.html">PEP 342</a>, but with a few differences. For one, you can send any signature, not just one object. You are able to pass any number of positional and keyword arguments through the send method. Also, this does not address a close method, but one could be easily added.
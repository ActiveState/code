## actorish decorator for making async code look more like sync one and a less blocking

Originally published: 2011-10-30 19:59:43
Last updated: 2011-10-30 19:59:44
Author: Przemyslaw Podczasi

I like how gevent is making async code to look like sync but non blocking without all the ugly callbacks.\nI tried doing that with threads and object proxy (I found great one at: http://pypi.python.org/pypi/ProxyTypes written by Phillip J. Eby, and this is where the actual magic happens).\n\nFor every function that is decorated it returns a proxy and the io call (or anything else) won't block until the value is actually needed.\n(should be some pools and args pickling there, to make it more like message passing but I  didn't want to fuzzy the example)\nTo use it as actor model, I guess it would require to queue requests to decorated object's methods and create a single thread to process them an in LazyProxy callback set q.get() instead of t.join()
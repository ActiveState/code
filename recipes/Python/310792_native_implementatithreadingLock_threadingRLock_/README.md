###A native implementation of threading.Lock and threading.RLock using Pyrex

Originally published: 2004-10-19 13:37:44
Last updated: 2004-10-19 13:37:44
Author: Nicolas Lehuen

Locks or mutexes are very basic primitives used to coordinate threads operations in multi-threaded programs. Unfortunately, even if Python provides a low-level implementation of locks in the thread module, the high level implementation of threading RLock is still in Python code, which is a bit worrying since locking is always a time critical task. This recipe implements both locks in Pyrex to get the speed of native code, and gives an example of how great Pyrex is.
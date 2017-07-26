## Yet another signal/slot implementation in Python

Originally published: 2008-09-01 23:21:28
Last updated: 2008-09-01 23:21:28
Author: Thiago Marcos P. Santos

This code snippet was based on the nice recipe 439356 made by Patrick Chasco. My implementation supports only class methods callbacks. I'm keeping the idea of use weakrefs to avoid the interpreter keep the object allocated because the signal is registered (i.e. the signal object holds a reference to callback method). IMO the usage of WeakValueDictionary made the code smaller and clear and also are maintenance-free (when the object is collect by the garbage collector the signal is automatically unregistered). 
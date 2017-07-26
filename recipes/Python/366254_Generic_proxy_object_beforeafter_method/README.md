## Generic proxy object with before/after method hooks.

Originally published: 2005-02-07 22:52:49
Last updated: 2005-02-07 22:52:49
Author: Martin Blais

A proxy object that delegates method calls to an instance, but that also calls hooks for that method on the proxy, or for all methods.  This can be used to implement logging of all method calls and values on an instance.
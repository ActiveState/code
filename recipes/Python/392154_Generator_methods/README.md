## Generator methods

Originally published: 2005-03-21 04:49:59
Last updated: 2005-03-25 15:58:44
Author: Peter Parente

This recipe enables the use of the yield statement within a method by decorating that method with a wrapper for a generator object. The purpose of using this decorator is to allow the method to be invoked using the normal calling syntax. A caller need not know the method is actually a generator and can focus solely on the method's interface rather than how it is implemented.
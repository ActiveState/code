###thread pool example #2 -- easy_pool class

Originally published: 2004-09-02 07:29:07
Last updated: 2004-09-08 13:48:11
Author: John Nielsen

I am trying to show how to have a thread pool\nbuilding on the recipe in http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/302746.\nThis is a python class that essentially makes a thread pool for a function you define.  Like the earlier example, I want to show off the power of having a thread pool that you can stop and start at will. Interestingly, you can mimic more standard thread use with the pool -- which I show off in as little as 3 lines of simple code.
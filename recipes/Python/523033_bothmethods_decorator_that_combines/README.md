###"bothmethods": decorator that combines staticmethod and classmethod

Originally published: 2007-07-08 19:01:33
Last updated: 2007-07-08 19:01:33
Author: Samuel Cormier-Iijima

I was looking for a way to have a method that when called on a class would get the class as its first argument, and when called on an instance would get that instance. Here is a nice way to do this (curry implementation thanks to http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/222061)
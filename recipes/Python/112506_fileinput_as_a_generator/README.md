## fileinput as a generator

Originally published: 2002-02-05 22:21:47
Last updated: 2002-02-09 23:25:26
Author: Brett Cannon

This is a basic re-implementation of fileinput using generators.  It supports all basic functionality that the library module has (nextfile(), lineno(), filelineno(), close(), and filename()).  It also adds an __iter__() method that is a generator.
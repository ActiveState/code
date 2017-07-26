## Create a restricted python function from a string

Originally published: 2008-03-01 13:08:11
Last updated: 2008-08-05 22:15:18
Author: david decotigny

The createFunction(sourceCode) below returns a python function that executes the given sourceCode (a string containing python code). The function, being a real python function, doesn't incur any overhead compared to any normal python function. And its environment is controlled: by default only safe operations are permitted (ie. map, reduce, filter, list, etc. ; others like import, open, close, eval, etc. are forbidden by default). But it is possible to extend this environment.
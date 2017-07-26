## Python Template Engine

Originally published: 2012-03-30 05:18:38
Last updated: 2012-03-31 21:28:12
Author: Sunjay Varma

This is a simple template engine which allows you to replace macros within text. This engine allows for attributes and filters. The default implementation provides the entire string module as filters. Trying to use arguments will of course not work (since the framework supports no other arguments for the filter other than the filtered string itself).
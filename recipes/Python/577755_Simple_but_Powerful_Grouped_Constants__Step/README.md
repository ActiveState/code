## Simple but Powerful Grouped Constants -- A Step Toward NamedConstants 
Originally published: 2011-06-14 20:19:14 
Last updated: 2011-08-12 23:21:32 
Author: Eric Snow 
 
The recipe provides an easy-to-use class for a group of "constants".  It provides helper functions for getting the constant values just right.  It also exposes the mechanism it uses to bind the contents of an iterable into the namespace of another object.\n\nFor this binding and for the grouped constants, this recipe makes it easy to dynamically generate the mapped values you want to expose.\n\nThe next step is to make the values aware of the context in which they are bound and to strengthen their association with the group they are in.  And that is one of the recipes I'm working on next!
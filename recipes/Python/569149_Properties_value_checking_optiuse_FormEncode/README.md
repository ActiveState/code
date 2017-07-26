## Properties with value checking with the option to use FormEncode validators.

Originally published: 2008-04-15 04:22:03
Last updated: 2008-04-19 11:22:13
Author: Markus Juenemann

The following recipe builds on the recipe "Using one method as accessor for multiple attributes" (Python Cookbook, p.752) which in turn seems to be based on  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/205126. It adds another argument which provides methods used to validate the value of a property. The interface is modeled after Ian Bicking's FormEncode package (http://formencode.org/). In fact the validators of the FormEncode package can be used as shown in the code below.
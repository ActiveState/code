## Automating simple property creation  
Originally published: 2002-10-21 06:29:23  
Last updated: 2003-09-07 04:49:13  
Author: Sean Ross  
  
The following are a set of functions for creating simple properties -
like Ruby's attr_reader, attr_writer, and attr_accessor.

If, inside a class definition, you write:

&nbsp &nbsp &nbsp &nbsp attribute(foo=1, bar=2)

simple properties named 'foo' and 'bar' are created for this class.
Also, private instance variables '__foo' and '__bar' will be added
to instances of this class.

By "simple properties", I mean something like the following:

&nbsp &nbsp &nbsp &nbsp ''' assume we're inside a class definition and
&nbsp &nbsp &nbsp &nbsp  self.__foo and self.__bar have been instantiated.
&nbsp &nbsp &nbsp &nbsp '''
&nbsp &nbsp &nbsp &nbsp def get_foo(self):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp return self.__foo
&nbsp &nbsp &nbsp &nbsp def set_foo(self, value):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp self.__foo = value
&nbsp &nbsp &nbsp &nbsp def del_foo(self):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp del self.__foo
&nbsp &nbsp &nbsp &nbsp def get_bar(self):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp return self.__bar
&nbsp &nbsp &nbsp &nbsp def set_bar(self, value):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp self.__bar = value
&nbsp &nbsp &nbsp &nbsp def del_bar(self):
&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp del self.__bar
&nbsp &nbsp &nbsp &nbsp foo = property(fget=get_foo, fset=set_foo, fdel=del_foo, doc="foo")
&nbsp &nbsp &nbsp &nbsp bar = property(fget=get_bar, fset=set_bar, fdel=del_bar, doc="bar")
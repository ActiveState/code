## Two quick functions for object introspection  
Originally published: 2017-01-14 22:35:16  
Last updated: 2017-01-14 22:35:17  
Author: Vasudev Ram  
  
This recipe shows two quick-and-clean :) utility functions for introspection of Python objects. They are meant to be used while working interactively in the reular Python shell or in the IPython shell. Both of them display attributes of any given object passed as the argument. The first function displays all attributes. The second function only displays atttributes that do not begin and end with a double underscore, so as to filter out "dunder" methods a.k.a. "special" methods - like __len__, __str__, __repr__, etc. The first function - oa(o) , where o is some object - does the same as dir(o), but is useful - in IPython - because, dir(o) output will scroll off the screen if the output is long, since it prints the attributes vertically, one per line, while oa(o) prints them horizontally, so has less chance of the output scrolling off, and the output also occupies fewer lines on the screen, so is easier to scan quickly. The second function - oar(o) - is like oa(o), but filters out attribute names that begin and end with a dunder. So it is useful in both IPython and Python.

More information and outputs here:

https://jugad2.blogspot.in/2017/01/two-simple-python-object-introspection.html


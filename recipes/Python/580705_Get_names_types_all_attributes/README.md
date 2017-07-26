## Get names and types of all attributes of a Python module  
Originally published: 2016-10-06 17:21:41  
Last updated: 2016-10-06 17:21:42  
Author: Vasudev Ram  
  
This recipe shows how to get the names and types of all the attributes of a Python module. This can be useful when exploring new modules (either built-in or third-party), because attributes are mostly a) data elements or b) functions or methods, and for either of those, you would like to know the type of the attribute, so that, if it is a data element, you can print it, and if it is a function or method, you can print its docstring to get brief help on its arguments, processsing and outputs or return values, as a way of learning how to use it.\n\nThe code for the recipe includes an example call to it, at the end of the code.\nNote that you first have to import the modules that you want to introspect in this way.\n
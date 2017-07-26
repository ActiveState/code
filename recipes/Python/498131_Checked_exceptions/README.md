## Checked exceptions 
Originally published: 2006-09-23 03:57:21 
Last updated: 2006-09-23 13:55:13 
Author: kay schluehr 
 
Checked exceptions are one of the most debated features of the Java language. A checked exception is a contract between a function that declares and throws an exception and another function that calls those function and has to handle the exception in its body. This recipe presents a checked exception implementation for Python using a pair of decorators @throws(Exc) and @catches(Exc,...). Whenever a @throws decorated function is called it has to be inside of a function that is decorated by @catches. Otherwise an UncheckedExceptionError will be raised - unless the declared exception Exc is raised.
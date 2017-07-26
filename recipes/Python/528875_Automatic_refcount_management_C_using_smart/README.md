## Automatic ref-count management in C++ using a smart ptrOriginally published: 2007-08-14 15:41:44 
Last updated: 2007-08-14 15:41:44 
Author: Ian Eloff 
 
Managing ref-counting is a complex and error prone business. If you choose C++ to extend or embed Python, you can simply use a modification on std::auto_ptr. Instead of calling delete on the managed pointer, it will decref it.\n\nSo now you can do:\n\nauto_py str = PyStr_FromString("Hello World!");\n\nand forget about having to decref it altogether! Just like auto_ptr you can get the PyObject * with get(), release it from managed control with release(), and rebind it with reset(new_ptr). You can also incref it by calling inc(), but be cautious as you can easily create a leak by increfing once to much.
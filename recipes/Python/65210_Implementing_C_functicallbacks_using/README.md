## Implementing C function callbacks using PythonOriginally published: 2001-06-14 20:35:36 
Last updated: 2001-06-19 15:01:52 
Author: pink chry 
 
Lets say you have a function in C or C++ that takes a function callback as an argument. You want to call this function by passing a Python function as the callback. This recipe shows the basics by calling the standard C library function qsort, and passing a python function as the compare function.
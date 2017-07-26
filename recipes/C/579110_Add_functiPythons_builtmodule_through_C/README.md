###Add function to Python's __builtin__ module through C API

Originally published: 2015-10-15 15:23:02
Last updated: 2015-10-16 12:11:58
Author: airween 

Add function to __builtin__ module through C API\n\nSometimes it need to embedding a Python script to a C code, and it references to a function, which also provided by the same C code. Then you have to import the module, as you defined in your C code.\n\nBut this import would be skipped, if you add your function to your __builtin__ module. In Python3 (3.5), there is the PyModule_AddFunctions() function, but in the previous versions, you can make it like this snippet.\n\nSee these recipes:\n\nMakefile:\nhttps://code.activestate.com/recipes/579111-add-function-to-__builtin__-module-through-c-api-c/\n\nPython script:\nhttps://code.activestate.com/recipes/579112-add-function-to-__builtin__-module-through-c-api-c/
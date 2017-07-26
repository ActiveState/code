## help in debugging memory problems  
Originally published: 2001-08-23 18:25:12  
Last updated: 2001-08-23 18:25:12  
Author: Will Ware  
  
When developing C extensions and running into memory problems, I find\nthe typical problem is mismanagement of reference\ncounts, particularly abuses of Py_INCREF and Py_DECREF, as well as\nforgetfulness of the refcount effects of functions like Py_BuildValue,\nPyArg_ParseTuple, PyTuple/List_SetItem/GetItem, etc. The\n1.5.2 source codebase offers some help with this (search for\nPy_TRACE_REFS) but I found it useful to add this function in\nObjects/object.c, just before _Py_PrintReferences.\n\nUnlike _Py_PrintReferences, this function will print only the total of\nall the refcounts in the system, so it can be used safely in loops that\nwill repeat millions of times, where_Py_PrintReferences would print out way too\nmuch stuff to be useful. This can help you to identify errantly wandering\nPy_INCREFs and Py_DECREFs.
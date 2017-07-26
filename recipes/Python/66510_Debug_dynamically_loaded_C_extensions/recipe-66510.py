The best way of finding core dumps with a Python extension is to compile
the extension source with '-g', and then follow these steps.  You may want to
re-compile any other extensions you use (like Numeric) with -g.

% gdb /usr/bin/python2.1
(gdb) br _PyImport_LoadDynamicModule 
(gdb) cont   # repeat until your extension is loaded


(gdb) finish # to load your extension
(gdb) br wrap_myfunction  # the entry point in your code
(gdb) disable 1   # don't want to break for more modules being loaded
(gdb) continue

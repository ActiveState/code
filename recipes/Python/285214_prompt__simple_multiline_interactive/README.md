## prompt - simple multiline interactive interpreter

Originally published: 2004-06-01 09:33:12
Last updated: 2004-06-01 09:33:12
Author: Carl Kleffner

The prompt module is a simple embedded multiline python interpreter built around raw_input(). The interpreter can be started at any given location in a program by executing a tiny code object and is allways executed in the namespace of the caller. Objects in the current scope can easily be explored and modified. Intermediate interruption of the control flow for manual interaction is handy for debugging purposes. The ability of multiline commands was crucial for me, so I wrote this module. It is tested with python, jython and stackless. The prompt codeobject can also be started from the pdb prompt.
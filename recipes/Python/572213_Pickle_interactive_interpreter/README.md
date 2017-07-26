## Pickle the interactive interpreter state  
Originally published: 2008-05-19 08:15:14  
Last updated: 2008-05-20 10:36:50  
Author: Oren Tirosh  
  
This code extends the pickle module to enable pickling of functions and classes defined interactively at the command prompt. You can save the interpreter state by pickling the __main__ module and restore it later.
## Clean a .py file full of constant chr(x) calls  
Originally published: 2010-04-02 08:20:49  
Last updated: 2010-04-02 08:20:50  
Author: Marcelo Fernández  
  
This script identifies every chr(xx) call in a script (being xx an integer) and replaces it with a constant byte string. For example: print chr(13) + chr(255) in the input .py file gets translated into '\\n' + '\\xff' on the output .py file, not breaking the input program, and maybe speeding it a little.
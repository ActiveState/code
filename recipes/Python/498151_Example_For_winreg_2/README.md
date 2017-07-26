## Example For winreg (2)  
Originally published: 2006-10-02 15:21:42  
Last updated: 2011-05-20 13:22:37  
Author: Stephen Chappell  
  
This recipe is another example of how to use the winreg module.
The code had the first purpose of demonstrating the concept of
a graphical shell built in Python. The shell was easily modified
to make use of the Window's registry but retains traces of its
original method of operation (all of which has been commented out).

The program down below originally used the pickle module to save
all of its settings when closing down. Now once the escape key is
pressed, this Python 2.5 program can use the module presented in
recipe 510392 to access Microsoft Window's Registry and store its
settings there. Check `do_exit` and `do_config` functions for usage.
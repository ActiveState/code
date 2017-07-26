###Adding the directory of the python executable to the system PATH under windows

Originally published: 2010-05-19 18:59:26
Last updated: 2010-05-19 19:01:31
Author: Anthon van der Neut

If you install python under windows and then open a command shell (DOS-prompt, you normally get an error message\nif you type "python" at the prompt. This is because the directory of the python executable is not in the PATH environment variable.\nIf you know where you installed python, you can add this via Control Panel -> System -> Advanced -> Environment Variables but this is not very user friendly way of doing things and error prone.\n\nThis program, if run by double clicking the file or by dragging the file to a command shell, will add the directory of the executable associated with the .py extension to the PATH env. var (if it is not already in there). It will notify other programs of this change, but unfortunately command.com is not smart enough to understand that. You have to open a new command shell after running the program in order to be able to run "python" at the dos prompt.\n\nIf run with the optional command line parameter 'remove' the directory will be removed from the PATH.
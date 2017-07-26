###Generate a Windows command file to execute a Python program

Originally published: 2005-02-08 14:16:06
Last updated: 2005-02-08 14:16:06
Author: Jim Jinkins

Generate a Windows command file that executes a Python program.  Typing\n'my_prog arg1 is easier than typing 'python C:\\PyLib\\my_prog.py arg1'.\nNeeded because Windows does not support '#!/bin/env python' as the first\nline of the program.
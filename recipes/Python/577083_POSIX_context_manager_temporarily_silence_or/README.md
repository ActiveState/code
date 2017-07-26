## POSIX context manager to temporarily silence, or filter lines from stdout 
Originally published: 2010-03-03 04:31:03 
Last updated: 2010-03-03 06:17:23 
Author: pwaller  
 
Fed up with libraries you don't have control over emitting text into your precious stdout?\n\nIf they use stdout through python, then you can just change sys.stdout to be something else. If they are printing directly to stdout through a C module, or some other means, then you are stuck.\n\n.. at least until you discover the `with silence():` block!\n\nCaveats: Non-portable, tested only on 2.6 under Linux, uses threading.\n\nExample output:\n\n    $ python silence_file.py \n    Before with block..\n    Sensible stuff!\n    After the silence block\n
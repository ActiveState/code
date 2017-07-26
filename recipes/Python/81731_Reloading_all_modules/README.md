## Reloading all modules 
Originally published: 2001-10-15 02:08:03 
Last updated: 2001-10-15 02:08:03 
Author: Sébastien Keim 
 
When you create a Python module, you can use a test script wich import your module. But you probably have noticed that when you run the test script, it always use the first version of your module even if you made changes in the code.\nThis is because the import statement check if the module is already in memory and do the import stuff only when this is mandated.\n\nYou can use the reload() function but this is quite difficult if you do changes in a module wich isn't directly imported by your test script.\n\nA good solution could be to remove all modules from memory before running the test script.\nYou only have to put some few lines at the start of your test script.
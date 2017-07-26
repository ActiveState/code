## Generate automatically list of actions with argparseOriginally published: 2011-11-14 20:16:53 
Last updated: 2011-12-02 10:25:13 
Author: Andrea Crotti 
 
This little sample script looks up in locals() to determine all the callables in *main*.\n\nThen it passes them to parse_arguments, which show an help message as following\nusage:\n \n    prova.py [-h] {func2,func1}\n\n    positional arguments:\n      {func2,func1}\n\n    optional arguments:\n      -h, --help     show this help message and exit\n\nUseful to avoid duplication and make it easy to extend script functions.
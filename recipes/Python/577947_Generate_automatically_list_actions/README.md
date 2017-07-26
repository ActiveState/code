## Generate automatically list of actions with argparse  
Originally published: 2011-11-14 20:16:53  
Last updated: 2011-12-02 10:25:13  
Author: Andrea Crotti  
  
This little sample script looks up in locals() to determine all the callables in *main*.

Then it passes them to parse_arguments, which show an help message as following
usage:
 
    prova.py [-h] {func2,func1}

    positional arguments:
      {func2,func1}

    optional arguments:
      -h, --help     show this help message and exit

Useful to avoid duplication and make it easy to extend script functions.
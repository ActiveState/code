## Filling command line arguments with a file  
Originally published: 2011-10-24 13:13:04  
Last updated: 2011-10-24 13:13:04  
Author: obernard78+activestate   
  
This is a recipe to populate command line args with the content of a file.

It is also an example of how to use the Action class from the argparse module.

I use this script in order to put frequently used options (such as  for the scripts I write in config files.
I created an abstract class in order to inherit from it to implement several file formats.
Choice has been taken not to keep the file name in parsed args, but it can be done by adding:
    setattr(namespace, self.dest, values)
at the end of the `__call__` method.

Test functions at the end (even if the ugliest I've ever written and seen) explains the way it works.
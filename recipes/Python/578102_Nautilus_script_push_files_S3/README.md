## Nautilus script to push files to S3 in python  
Originally published: 2012-04-10 21:41:48  
Last updated: 2012-04-10 21:41:48  
Author: coleifer@gmail.com   
  
A small script that allows you to push files and directories to S3 using a context menu in nautilus file browser.\n\nAdd this script to ``~/.gnome2/nautilus-scripts/`` and be sure it is executable.  Requires [boto](http://boto.readthedocs.org/), the python aws library.  Credentials by default are looked up from ~/.boto but can be supplied in the get_s3_conn() function.
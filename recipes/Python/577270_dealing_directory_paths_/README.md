## dealing with directory paths with ~  
Originally published: 2010-06-16 22:45:18  
Last updated: 2010-06-16 23:17:20  
Author: roopeshv   
  
Dealing with directory paths which start with `~` which are passed as paramaters, to `os` module functions.

Here is what I think python doesn't do for me:

    >>> import os
    # suppose my home = curdir = /home/rv
    >>> os.path.abspath('.') 
    '/home/rv'

Now if I want to go to folder `/home/rv/test` if there is no folder by name 
/home/rv/~/test/

    # This is what happens by default.
    >>> os.path.abspath('~/test')
    '/home/rv/~/test'
    
    >>> os.chdir('/home/rv/some/dir')
    # doesn't matter if the resulting path exists or not.
    >>> os.path.abspath('~/test')
    'home/rv/some/dir/~/test'

This would be more sensible I guess:

    # if /home/rv/~/test doesn't exist
    >>> os.path.abspath('~/test')
    '/home/rv/test'
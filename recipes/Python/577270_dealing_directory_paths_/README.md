###dealing with directory paths with ~

Originally published: 2010-06-16 22:45:18
Last updated: 2010-06-16 23:17:20
Author: roopeshv 

Dealing with directory paths which start with `~` which are passed as paramaters, to `os` module functions.\n\nHere is what I think python doesn't do for me:\n\n    >>> import os\n    # suppose my home = curdir = /home/rv\n    >>> os.path.abspath('.') \n    '/home/rv'\n\nNow if I want to go to folder `/home/rv/test` if there is no folder by name \n/home/rv/~/test/\n\n    # This is what happens by default.\n    >>> os.path.abspath('~/test')\n    '/home/rv/~/test'\n    \n    >>> os.chdir('/home/rv/some/dir')\n    # doesn't matter if the resulting path exists or not.\n    >>> os.path.abspath('~/test')\n    'home/rv/some/dir/~/test'\n\nThis would be more sensible I guess:\n\n    # if /home/rv/~/test doesn't exist\n    >>> os.path.abspath('~/test')\n    '/home/rv/test'
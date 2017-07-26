## Move files with rename if required  
Originally published: 2012-04-30 11:08:13  
Last updated: 2012-04-30 11:09:05  
Author: John Reid  
  
A python script that renames (moves) files to a destination
directory. However it will not overwrite existing files. The
script uses a renaming strategy where a count is incremented
in order to avoid naming conflicts.

Example usage::

    mv-rename a.ext b.ext target-dir/

would mv a.ext and b.ext into the target directory. If::

    target-dir/a.ext
    target-dir/b.ext

already exist, the newly moved files would be named::

    target-dir/a-<N>.ext
    target-dir/b-<M>.ext

where <N> and <M> are the lowest numbers such that there
is no conflict.

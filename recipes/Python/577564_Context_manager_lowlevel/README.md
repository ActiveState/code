###Context manager for low-level redirection of stdout/stderr

Originally published: 2011-02-06 02:36:32
Last updated: 2012-01-26 02:14:25
Author: Greg Haskins

This context manager provides a convenient, Pythonic way to temporarily replace the file descriptors of `stdout` and `stderr`, redirecting to either `os.devnull` or files of your choosing. Swapping the C-level file descriptors is required when suppressing output from compiled extension modules, such as those built using F2PY. It functions equally well for pure-Python code. *UPDATE:* (see below).
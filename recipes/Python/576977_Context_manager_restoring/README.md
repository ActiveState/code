## Context manager for restoring a value  
Originally published: 2009-12-04 09:12:59  
Last updated: 2010-01-09 07:14:06  
Author: George Sakkis  
  
Often one wants to rebind a name or modify a mutable object, perform a bunch of actions and finally restore the name/object to its original state. An example is redirecting stdout/stderr temporarily (http://www.diveintopython.org/scripts_and_streams/stdin_stdout_stderr.html). The *restoring* context manager shown below simplifies this pattern::

    import sys

    # prints in console
    print "hello world!"

    with restoring('sys.stdout'):
        with open('hello.txt', 'w') as sys.stdout:
            # prints in file
            print "hello world!"

    # prints in console again
    print "hello world!"

## Context manager for restoring a valueOriginally published: 2009-12-04 09:12:59 
Last updated: 2010-01-09 07:14:06 
Author: George Sakkis 
 
Often one wants to rebind a name or modify a mutable object, perform a bunch of actions and finally restore the name/object to its original state. An example is redirecting stdout/stderr temporarily (http://www.diveintopython.org/scripts_and_streams/stdin_stdout_stderr.html). The *restoring* context manager shown below simplifies this pattern::\n\n    import sys\n\n    # prints in console\n    print "hello world!"\n\n    with restoring('sys.stdout'):\n        with open('hello.txt', 'w') as sys.stdout:\n            # prints in file\n            print "hello world!"\n\n    # prints in console again\n    print "hello world!"\n
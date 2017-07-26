###Use simple command-line options to effect program runtime.

Originally published: 2001-03-03 10:37:03
Last updated: 2001-03-03 10:37:03
Author: Chris McDonough

Using sys.argv and globals(), you can build scripts which can modify their behavior at runtime based on arguments passed on the command line.  This script, 'test_test.py' is built to be run from the command line.  It allows you to invoke the script without any command-line arguments, in which case, the main() function is run.  However, if the script is invoked via "python test_test.py debug", the debug function is run instead.  This script uses Stephen Purcell's 'unittest' module from his PyUnit unit testing framework.
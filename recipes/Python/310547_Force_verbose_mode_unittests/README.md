## Force verbose mode for unittests in an IDE.

Originally published: 2004-10-18 01:34:39
Last updated: 2004-10-18 01:34:39
Author: Jason Whitlark

When running unit tests, using the verbose flag often provides an extra level of protection against mistakes.  When running from the command line, this simply means adding the v option.  If you use an IDE, matters become more complicated.  While you can often set your IDE to pass in the v option when running a file, this has a number of drawbacks.  This code will ensure that your tests will run with the verbose option.
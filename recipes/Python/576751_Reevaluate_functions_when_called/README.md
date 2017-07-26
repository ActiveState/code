###Reevaluate functions when called

Originally published: 2009-05-13 15:49:32
Last updated: 2009-05-13 15:53:28
Author: geremy condra

This small snippet came about as a result of [this discussion](http://groups.google.com/group/python-ideas/browse_thread/thread/92cf3f55919a8510/9e39950144daa9bb) on python-ideas, requesting a new syntax for dynamically reevaluating a function each time it is called.\n\nThis snippet implements a simple decorator to do so without added syntax.
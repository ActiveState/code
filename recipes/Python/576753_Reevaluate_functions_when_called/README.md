## Reevaluate functions when called, v2

Originally published: 2009-05-14 15:10:51
Last updated: 2009-05-14 15:10:51
Author: geremy condra

As with version 1 of this recipe, it was sparked by a discussion on python-ideas about adding a special syntax to function signatures for reevaluating the arguments to a function at runtime. The below is a decorator and annotation based solution to this problem which stores the code to be evaluated as a string in the annotations, rather than reevaluating the entire function every time it is called.
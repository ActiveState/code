## Reevaluate functions when called, v3 
Originally published: 2009-05-14 15:17:23 
Last updated: 2009-05-14 15:18:41 
Author: geremy condra 
 
This small snippet came about as a result of this discussion on python-ideas, requesting a new syntax for dynamically reevaluating a function each time it is called.\n\nIt is a minor alteration of version 2 of this recipe that, instead of calling eval() on string annotations, simply requires that the annotations be callable and calls them at runtime.
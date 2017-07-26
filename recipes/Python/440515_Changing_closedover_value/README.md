## Changing a closed-over value (in a "cell")  
Originally published: 2005-09-02 18:40:43  
Last updated: 2005-09-02 18:40:43  
Author: paul cannon  
  
In most languages with closures, it is possible to change a closed-over value and have the change visible in other closures which share a reference to the same variable.  Python's syntax makes this impossible.\n\nEven if you're content (I am) with the work-around-- putting your changeable values inside a mutable object like a list-- it may occasionally happen that you wish you could change the closed-over values, found in "cell" objects in a function's func_closure tuple.  Another recipe I submitted shows how to get at the values in standard Python; this one will demonstrate a way to actually change that value, so that functions which also close over that value (share a reference to the same cell) will see the change.
## weakmethod  
Originally published: 2006-09-29 01:45:31  
Last updated: 2006-09-29 01:45:31  
Author: tomer filiba  
  
Weakly-bound methods: use this decorator to create methods that weakly-reference their instance (im_self). This means that the method itself will not keep the object alive. Useful for callbacks, caches, and avoiding cyclic references.
## Highly branched Trees  
Originally published: 2014-05-14 18:23:41  
Last updated: 2014-05-14 19:16:04  
Author: Chris Ecker  
  
Trees are very common data structures and are usually considered to be very efficient. However, this is only true if the tree is balanced, meaning that all branches have roughly the same number of nodes. \n\nThere are good balancing trees, such as rb-trees or avl-trees. Unfortunately they are quite difficult to implement. An alternative tree structure is the highly branched b-tree (https://en.wikipedia.org/wiki/B-tree). In the c language, binary trees are preferable in most cases. However, in python things are different. This recipe shows how simple it is to implement a b-tree in python. The example is a sorted dict.
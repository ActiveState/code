## Non-recursive (and non-tracking) traversal of a (DOM) tree 
Originally published: 2005-12-08 08:25:14 
Last updated: 2005-12-14 16:57:54 
Author: Henry James 
 
A methode to traverse a tree (or the rest of a tree starting from a node with unkown position) depth-first without recursion and without mandatorily keeping track of the position of the current node; requires each node to have reference acess to its parent, first child and next sibling, therefore especially suitable for DOM trees.
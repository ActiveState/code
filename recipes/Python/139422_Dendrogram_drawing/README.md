## Dendrogram drawing 
Originally published: 2002-07-13 21:17:10 
Last updated: 2002-07-13 21:17:10 
Author: David Eppstein 
 
This recipe draws a dendrogram (horizontal format used for evolutionary trees), as ASCII text, given as input a binary tree in the form of a tuple for each tree node.  Tree leaves can be any Python object other than a length-2 tuple, and are converted to strings in the output.  Tree nodes at the same distance from the root will line up at the same column, with the distance between tree levels controlled by an optional "sep" parameter. The algorithm works by a straightforward inorder traversal, keeping some simple data structures to keep track of the tree edges that need to be drawn on each output line.  Its output is via print statements but it could easily be modified to send its output lines to any other kind of stream.
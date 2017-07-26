## Sharing-aware tree transformations  
Originally published: 2012-05-02 15:10:35  
Last updated: 2012-05-07 08:20:58  
Author: Sander Evers  
  
The function `foldsh` in this recipe is a general purpose tool for transforming tree-like recursive data structures while keeping track of shared subtrees.

    # By default, a branch is encoded as a list of subtrees; each subtree can be a
    # branch or a leaf (=anything non-iterable). Subtrees can be shared:
    >>> subtree = [42,44]
    >>> tree = [subtree,[subtree]]
    # We can apply a function to all leaves:
    >>> foldsh(tree, leaf= lambda x: x+1)
    [[43, 45], [[43, 45]]]
    # Or apply a function to the branches:
    >>> foldsh(tree, branch= lambda t,c: list(reversed(c)))
    [[[44, 42]], [44, 42]]
    # The sharing is preserved:
    >>> _[0][0] is _[1]
    True
    # Summing up the leaves without double counting of shared subtrees:
    >>> foldsh(tree, branch= lambda t,c: sum(c), shared= lambda x: 0)
    86

In particular, it is useful for transforming YAML documents. An example of this is given below.
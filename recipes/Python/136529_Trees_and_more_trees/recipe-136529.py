"""
This module implements binary and generalized trees.

History of changes:
version 1.1:
 - Changed cargo, left/right props of InsertionBTree to be read-only.
 - find and delete methods for InsertionBTree.
 - Introduced empty trees (trees with no nodes).
 - Deleted not implemented's from abstract classes.
 - Deleted some if redundant checks.

ToDo:
 - Make empty tree a cached "static" value?
 - Move graft/ungraft to be methods of childs prop, now returning a
   set-like object?
"""


#Import generators.
from __future__ import generators


__version__ = 1.1
__author__ = "G. Rodrigues"


#Auxiliary class to tackle default args.
class _undef_arg(object):
    pass


#The abstract BTree class, where most of the methods reside.
class AbstractBTree(object):
    """The binary tree "interface" class.

    It has three properties: cargo, and the left and right subtrees.
    A terminal node (= atomic tree) is one where the left and right
    subtrees are the empty tree."""

    def IsAtom(self):
        """Returns 1 if the tree has no nonempty subtrees, 0 otherwise."""
        if self:
            if self.left or self.right:
                return 0
            else:
                return 1
        else:
            return 1

    #The simplest print possible.
    def __str__(self):
        if not self:
            return "()"
        else:
            return "(%s, %s, %s)" % (str(self.cargo), str(self.left), str(self.right))

    #The BTree iterators.
    def __iter__(self):
        """The standard preorder traversal of a binary tree."""
        if self:
            yield self.cargo
            for elem in self.left:
                yield elem
            for elem in self.right:
                yield elem

    def postorder(self):
        """Postorder traversal of a binary tree."""
        if self:
            for elem in self.left.postorder():
                yield elem
            for elem in self.right.postorder():
                yield elem
            yield self.cargo
        
    def inorder(self):
        """Inorder traversal of a binary tree."""
        if self:
            for elem in self.left.inorder():
                yield elem
            yield self.cargo
            for elem in self.right.inorder():
                yield elem

    #"Inplace" iterators.
    def subtree(self):
        """Preorder iterator over the (nonempty) subtrees.

        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""

        if self:
            yield self
            for tree in self.left.subtree():
                yield tree
            for tree in self.right.subtree():
                yield tree

    def postsubtree(self):
        """Postorder iterator over the (nonempty) subtrees.

        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""        

        if self:
            for tree in self.left.postsubtree():
                yield tree
            for tree in self.right.postsubtree():
                yield tree
            yield self

    def insubtree(self):
        """Inorder iterator over the (nonempty) subtrees.

        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""        

        if self:
            for tree in self.left.postsubtree():
                yield tree
            yield self
            for tree in self.right.postsubtree():
                yield tree

    #Binary comparisons.
    def __eq__(self, other):
        """Checks for equality of two binary trees."""
        #Both trees not empty.
        if self and other:
            #Compare cargos.
            if self.cargo != other.cargo:
                return 0
            else:
                #Recursive calls.
                if self.left.__eq__(other.left):
                    return self.right.__eq__(other.right)
                else:
                    return 0
        #Both trees empty.
        elif not self and not other:
            return 1
        else:
            return 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, elem):
        """Returns 1 if elem is in some node of the tree, 0 otherwise."""
        for element in self:
            if elem == element:
                return 1
        return 0

    def __len__(self):
        """Returns the number of nodes (elements) in the tree."""
        ret = 0
        for elem in self:
            ret += 1
        return ret

    def copy(self):
        """Shallow copy of a BTree object."""
        if self:
            return self.__class__(self.cargo, self.left.copy(), self.right.copy())
        else:
            return self.__class__()


#The two implementations of BTree class.
class MutableBTree(AbstractBTree):
    """A mutable implementation of the binary tree BTree class."""

    def __init__(self, cargo = _undef_arg, left = None, right = None):
        """The initializer."""
        if cargo is not _undef_arg:
            self.__cargo = cargo

            if left is not None:
                if isinstance(left, MutableBTree):
                    self.__left = left
                else:
                    raise TypeError, "Object %s is not a MutableBTree binary tree." % repr(left)
            else:
                self.__left = MutableBTree()

            if right is not None:
                if isinstance(right, MutableBTree):
                    self.__right = right
                else:
                    raise TypeError, "Object %s is not a MutableBTree binary tree." % repr(right)
            else:
                self.__right = MutableBTree()

    def __nonzero__(self):
        """Returns 1 if the tree is nonempty, 0 otherwise."""
        try:
            self.__cargo
            return 1
        except AttributeError:
            return 0

    #Properties.
    def __get_cargo(self):
        if self:
            return self.__cargo
        else:
            raise AttributeError, "An empty tree has no cargo."

    def __set_cargo(self, cargo):
        if not self:
            self.__left = MutableBTree()
            self.__right = MutableBTree()            
        self.__cargo = cargo

    def __del_cargo(self):
        if self:
            #Turn tree into an empty tree => delete all attributes.
            del self.__cargo
            del self.__left
            del self.__right
        else:
            raise AttributeError, "Cannot delete the cargo of an empty tree."

    cargo = property(__get_cargo, __set_cargo, __del_cargo, "The root element of the tree.")

    def __get_left(self):
        if self:
            return self.__left
        else:
            raise AttributeError, "An empty tree has no left subtree."

    def __set_left(self, tree):
        if self:
            if isinstance(tree, MutableBTree):
                self.__left = tree
            else:
                raise TypeError, "Object %s is not a MutableBTree." % repr(tree)
        else:
            raise AttributeError, "Cannot set the left subtree of an empty tree."

    def __del_left(self):
        if self:
            self.__left = MutableBTree()
        else:
            raise AttributeError, "Cannot delete the left subtree of an empty tree."

    left = property(__get_left, __set_left, __del_left, "The left subtree.")

    def __get_right(self):
        if self:
            return self.__right
        else:
            raise AttributeError, "An empty tree has no right subtree."

    def __set_right(self, tree):
        if self:
            if isinstance(tree, MutableBTree):
                self.__right = tree
            else:
                raise TypeError, "Object %s is not a MutableBTree." % repr(tree)
        else:
            raise AttributeError, "Cannot set the right subtree of an empty tree."

    def __del_right(self):
        if self:
            self.__right = MutableBTree()
        else:
            raise AttributeError, "Cannot delete the right subtree of an empty tree."

    right = property(__get_right, __set_right, __del_right, "The right subtree.")

    #General inplace transformations of mutable binary trees.
    def map(self, func):
        """Inplace map transformation of a binary tree."""
        for tree in self.subtree():
            tree.cargo = func(tree.cargo)

    def ToImmutableBTree(self):
        """Returns an ImmutableBTree copy."""
        if self:
            return ImmutableBTree(self.cargo, self.left.ToImmutableBTree(), self.right.ToImmutableBTree())
        else:
            return ImmutableBTree()


class InsertionBTree(MutableBTree):
    """Class implementing insertion binary trees.

    The cargo, left and right properties are read-only. To add elements use the
    insert method.

    It is up to the client to ensure that the elements in the tree have meaningful
    order methods."""

    def __init__(self, cargo = _undef_arg):
        if cargo is _undef_arg:
            MutableBTree.__init__(self)
        else:
            MutableBTree.__init__(self, cargo)
            MutableBTree.left.__set__(self, InsertionBTree())
            MutableBTree.right.__set__(self, InsertionBTree())            

    #Redefinition of cargo, left/right properties to be read only.
    cargo = property(MutableBTree.cargo.__get__, None, None, "The root element of the tree.")
    left = property(MutableBTree.left.__get__, None, None, "The left subtree.")
    right = property(MutableBTree.right.__get__, None, None, "The right subtree.")

    #Redefinition of basic iterators.
    def __iter__(self):
        """Iterator over the tree elements in min-max order."""
        return MutableBTree.inorder(self)

    def subtree(self):
        """Traversal through the (nonempty) subtrees in min-max order.
        
        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""

        return MutableBTree.insubtree(self)

    #Iterating in max-min order.
    def inrevorder(self):
        """Iterator over the tree elements in max-min order."""
        if self:
            for elem in self.right.inrevorder():
                yield elem
            yield self.cargo
            for elem in self.left.inrevorder():
                yield elem

    def inrevsubtree(self):
        """Traversal through the (nonempty) subtrees in max-min order.
        
        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""

        if self:
            for tree in self.right.inrevsubtree():
                yield tree
            yield self
            for tree in self.left.inrevsubtree():
                yield tree

    #The in protocol.
    def __contains__(self, elem):
        if self:
            if elem == self.cargo:
                return 1
            elif elem > self.cargo:
                return self.right.__contains__(elem)
            else:
                return self.left.__contains__(elem)
        else:
            return 0

    def find(self, elem):
        """Returns the subtree which has elem as cargo.

        If elem is not in tree it raises an exception."""

        if self:
            if elem == self.cargo:
                return self
            elif elem > self.cargo:
                return self.right.find(elem)
            else:
                return self.left.find(elem)
        else:
            raise ValueError, "%s is not in tree." % str(elem)

    def insert(self, elem):
        """Inserts an element in the tree if it is not there already."""
        if not self:
            #Insert elem in empty tree.
            MutableBTree.cargo.__set__(self, elem)
            MutableBTree.left.__set__(self, InsertionBTree())
            MutableBTree.right.__set__(self, InsertionBTree())
        #Recursive calls.
        elif elem < self.cargo:
            self.left.insert(elem)
        elif elem > self.cargo:
            self.right.insert(elem)
            
    def delete(self, elem):
        """Deletes an elem from the tree.

        Raises an exception if elem is not in tree."""

        if self:
            if elem == self.cargo:
                if self.IsAtom():
                    MutableBTree.cargo.__del__(self)
                #Both trees not empty
                elif self.left and self.right:
                    #Get min element subtree and connect it to self.left.
                    minsubtree = self.right.subtree().next()
                    MutableBTree.left.__set__(minsubtree, self.left)
                    #root -> root.right.
                    MutableBTree.cargo.__set__(self, self.right.cargo)
                    MutableBTree.left.__set__(self, self.right.left)
                    MutableBTree.right.__set__(self, self.right.right)                    
                #Right subtree is empty.
                elif not self.right:
                    #root -> root.left
                    MutableBTree.cargo.__set__(self, self.left.cargo)
                    MutableBTree.left.__set__(self, self.left.left)
                    MutableBTree.right.__set__(self, self.left.right)
                #Left subtree is empty.
                else:
                    #root -> root.right
                    MutableBTree.cargo.__set__(self, self.right.cargo)
                    MutableBTree.left.__set__(self, self.right.left)
                    MutableBTree.right.__set__(self, self.right.right)
            #Recursive calls.
            elif elem < self.cargo:
                self.left.delete(elem)
            else:
                self.right.delete(elem)
        else:
            raise ValueError, "%s is not an element of the tree." % str(elem)


class ImmutableBTree(AbstractBTree):
    """An implementation of an immutable binary tree using tuples."""

    def __init__(self, cargo = _undef_arg, left = None, right = None):
        """The initializer."""
        if cargo is not _undef_arg:
            if left is not None:
                if not isinstance(left, ImmutableBTree):
                    raise TypeError, "Object %s is not an ImmutableBTree." % repr(left)
            else:
                left = ImmutableBTree()

            if right is not None:
                if not isinstance(right, ImmutableBTree):
                    raise TypeError, "Object %s is not an ImmutableBTree." % repr(right)
            else:
                right = ImmutableBTree()

            self.__head = (cargo, left, right)            
        else:
            self.__head = None

    def __nonzero__(self):
        """Returns 1 if the tree is nonempty, 0 otherwise."""
        return self.__head is not None

    #Properties.
    def __get_cargo(self):
        if self:
            return self.__head[0]
        else:
            raise AttributeError, "An empty tree has no cargo."

    cargo = property(__get_cargo, None, None, "The root element of the tree.")

    def __get_left(self):
        if self:
            return self.__head[1]
        else:
            raise AttributeError, "An empty tree has no left subtree."

    left = property(__get_left, None, None, "The left subtree.")

    def __get_right(self):
        if self:
            return self.__head[2]
        else:
            raise AttributeError, "An empty tree has no right subtree."

    right = property(__get_right, None, None, "The right subtree.")

    #Conversion method.
    def ToMutableBTree(self):
        """Returns a MutableBTree copy."""
        if self:
            return MutableBTree(self.cargo, self.left.ToMutableBTree(), self.right.ToMutableBTree())
        else:
            return MutableBTree()


#Making ImmutableBTree hashable.
class HashBTree(ImmutableBTree):
    """Class implementing a hashable immutable binary tree. It can contain only hashables."""

    def __init__(self, cargo = _undef_arg, left = None, right = None):
        try:
            if cargo is not _undef_arg:
                cargo.__hash__
            ImmutableBTree.__init__(self, cargo, left, right)
        except AttributeError:
            raise TypeError, "Object %s is not hashable." % repr(cargo)

    #HashBTrees can be keys in dictionaries (rhyme not intended).
    def __hash__(self):
        return hash(tuple(self))


#The abstract generalized tree class where most of the methods reside.
class AbstractTree(object):
    """The generalized "interface" tree class.

    It has two properties: the cargo and a childs iterator giving the child subtrees.

    The childs property returns a new (reset) iterator each time it is called.
    There is no order of iteration through the nodes (implementation is free to
    swap them around). """

    def IsAtom(self):
        """A tree is atomic if it has no subtrees."""
        try:
            self.childs.next()
        except StopIteration:
            return 1
        except AttributeError:
            return 1
        return 0

    #The simplest print possible.
    def __str__(self):
        if self:
            if self.IsAtom():
                return "(%s)" % str(self.cargo)
            else:
                temp = [str(subtree) for subtree in self.childs]
                return "(%s, %s)" % (str(self.cargo), ", ".join(temp))
        else:
            return "()"

    #The Tree iterators.
    def __iter__(self):
        """The standard preorder traversal iterator."""
        if self:
            yield self.cargo
            for subtree in self.childs:
                for elem in subtree:
                    yield elem

    def postorder(self):
        """Postorder traversal of a tree."""
        if self:
            for subtree in self.childs:
                for elem in subtree.postorder():
                    yield elem
            yield self.cargo

    #The "inplace" iterators.
    def subtree(self):
        """Preorder iterator over the subtrees.

        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""

        if self:
            yield self
            for subtree in self.childs:
                for tree in subtree.subtree():
                    yield tree

    def postsubtree(self):
        """Postorder iterator over the subtrees.

        Warning: As always, do not use this iterator in a for loop while altering
        the structure of the tree."""

        if self:
            for subtree in self.childs:
                for tree in subtree.postsubtree():
                    yield tree
            yield self

    #The in protocol.
    def __contains__(self, elem):
        """Returns 1 if elem is in the tree, 0 otherwise."""
        for element in self:
            if elem == element:
                return 1
        return 0

    #Number of elements in the tree.
    def __len__(self):
        """Returns the number of elements (nodes) in the tree."""
        ret = 0
        for elem in self:
            ret += 1
        return ret

    def copy(self):
        """Shallow copy of a Tree object."""
        if self:
            if self.IsAtom():
                return self.__class__(self.cargo)
            else:
                temp = tuple([subtree.copy() for subtree in self.childs])
                return self.__class__(self.cargo, *temp)
        else:
            return self.__class__()


#Tree implementations.
class MutableTree(AbstractTree):
    """Class implementing a mutable tree type."""

    def __init__(self, cargo = _undef_arg, *trees):
        """The initializer."""
        if cargo is not _undef_arg:
            self.__head = [cargo]
            if trees:
                for tree in trees:
                    if not isinstance(tree, MutableTree):
                        raise TypeError, "%s is not a MutableTree instance." % repr(tree)
                self.__head.extend(list(trees))
        else:
            self.__head = None

    def __nonzero__(self):
        return self.__head is not None

    #Properties.
    def __get_cargo(self):
        if self:
            return self.__head[0]
        else:
            raise AttributeError, "An empty tree has no cargo."

    def __set_cargo(self, cargo):
        if self:
            self.__head[0] = cargo
        else:
            self.__head = [cargo]

    def __del_cargo(self):
        if self:
            self.__head = None
        else:
            raise ValueError, "Cannot delete the cargo of an empty tree."

    cargo = property(__get_cargo, __set_cargo, __del_cargo, "The root element of the tree.")

    def __get_childs(self):
        def it(lst):
            for i in xrange(1, len(lst)):
                yield lst[i]

        if self:
            return it(self.__head)
        #Return empty iterator.
        else:
            return iter([])

    childs = property(__get_childs, None, None, "The iterator over the child subtrees.")

    #Add or delete trees to the root of the tree.
    def graft(self, tree):
        """Graft a tree to the root node."""
        if self:
            if isinstance(tree, MutableTree):
                self.__head.append(tree)
            else:
                raise TypeError, "%s is not a Tree instance." % repr(tree)
        else:
            raise AttributeError, "Cannot graft a tree in an empty tree."

    def ungraft(self, tree):
        """Ungrafts a subtree from the current node.

        The argument is the subtree to ungraft itself."""

        if self:
            for pair in zip(self.childs, range(1, len(self.__head))):
                if tree is pair[0]:
                    del self.__head[pair[1]]
                    return None
            raise AttributeError, "Tree %s is not grafted to the root node of this tree." % repr(tree)
        else:
            raise AttributeError, "Cannot ungraft a tree from an empty tree."

    #General inplace transformations of trees.
    def map(self, func):
        """Inplace map transformation of a tree."""
        for tree in self.subtree():
            tree.cargo = func(tree.cargo)

    #Conversion methods.
    def ToImmutableTree(self):
        """Convert tree into an immutable tree."""
        if self:
            if self.IsAtom():
                return ImmutableTree(self.cargo)
            else:
                temp = tuple([subtree.ToImmutableTree() for subtree in self.childs])
                return ImmutableTree(self.cargo, *temp)
        else:
            return ImmutableTree()


class ImmutableTree(AbstractTree):
    """Class implementing an immutable generalized tree type."""

    def __init__(self, cargo = _undef_arg, *trees):
        """The initializer."""
        if cargo is not _undef_arg:
            if trees:
                for tree in trees:
                    if not isinstance(tree, ImmutableTree):
                        raise TypeError, "%s is not a ImmutableTree instance." % repr(tree)
                self.__head = (cargo,) + trees
            else:
                self.__head = (cargo,)
        else:
            self.__head = None

    def __nonzero__(self):
        return self.__head is not None

    #Properties.
    def __get_cargo(self):
        if self:
            return self.__head[0]
        else:
            raise AttributeError, "An empty tree has no cargo."

    cargo = property(__get_cargo, None, None, "The root element of the tree")

    def __get_childs(self):
        def it(lst):
            for i in xrange(1, len(lst)):
                yield lst[i]

        if self:
            return it(self.__head)
        else:
            #Return empty iterator.
            return iter(())

    childs = property(__get_childs, None, None, "The iterator over the child subtrees.")

    def ToMutableTree(self):
        """Convert tree into a mutable tree."""
        if self:
            if self.IsAtom():
                return MutableTree(self.cargo)
            else:
                temp = tuple([subtree.ToMutableTree() for subtree in self.childs])
                return MutableTree(self.cargo, *temp)
        else:
            return MutableTree()

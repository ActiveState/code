"""
The Tree module implementing generalized trees.
"""

#Import generators.
from __future__ import generators


__version__ = '0.9.1'
__needs__ = '2.2'
__author__ = "G. Rodrigues"


#Classes
class MetaTree(type):
    """The MetaTree metaclass.

    A metaclass governing the family of generalized trees parameterized
    by a node class.

    Minimal protocol description of parameter node class:
    It's a class defining __iter__ (but check code below). The
    initializer takes an iterable as argument. There is no defined order
    of iteration over the subtrees - implementation is free to muck with
    it."""

    class MTree(object):
        """The mixin MTree class, containing generic tree methods."""

        def isAtom(self):
            """Return True if it has no subtrees, False otherwise."""
            if self:
                #ToDo: Ask node class to implement __nonzero__ to avoid
                #this test?
                iterator = iter(self.subtrees)
                try:
                    iterator.next()
                except StopIteration:
                    ret = True
                else:
                    ret = False
            else:
                ret = True
            return ret

        #The Tree iterators.
        def __iter__(self):
            """The standard preorder traversal iterator."""
            if self:
                yield self.cargo
                for subtree in self.subtrees:
                    for elem in subtree:
                        yield elem

        def postorder(self):
            """Postorder traversal of a tree."""
            if self:
                for subtree in self.subtrees:
                    for elem in subtree.postorder():
                        yield elem
                yield self.cargo

        #The "inplace" iterators.
        def presubtree(self):
            """Preorder iterator over the subtrees.

            Warning: As always, do not use this iterator in a for loop
            while altering the structure of the tree."""

            if self:
                yield self
                for subtree in self.subtrees:
                    for tree in subtree.presubtree():
                        yield tree

        def postsubtree(self):
            """Postorder iterator over the subtrees.

            Warning: As always, do not use this iterator in a for loop
            while altering the structure of the tree."""

            if self:
                for subtree in self.subtrees:
                    for tree in subtree.postsubtree():
                        yield tree
                yield self

        def copy(self, cls = None):
            """Shallow copy of a tree.

            An extra class argument can be given to copy with a different
            (tree) class. No checks are made on the class."""
            if cls is None:
                cls = self.__class__
            if self:
                subtrees = tuple([subtree.copy(cls) for subtree in \
                                  self.subtrees])
                return cls(self.cargo, *subtrees)
            else:
                return cls()

    #Metaclass instance methods.
    def __init__(cls, name, bases, dct):
        """The initializer."""
        node = dct.get('Node')
        #Replace Node attribute.
        if node is not None:
            #Some early protocol checks.
            if not callable(node):
                raise TypeError("Object not callable", node)
            try:
                node.__iter__
            except AttributeError:
                #Valid node classes like list, tuple dont have __iter__.
                #ToDo: Ditch this (brittle) test in 2.3.
                try:
                    iter(node(()))
                except TypeError:
                    raise TypeError("Object does not define __iter__", node)
            del dct['Node']
        else:
            #Default node class.
            node = list
        #Call super initializer.
        super(MetaTree, cls).__init__(name, bases, dct)
        #Set *private* attribute.
        cls.__node = node
        #Inject methods if class (or super classes) do not define it.
        for name in MetaTree.MTree.__dict__:
            generic = MetaTree.MTree.__dict__[name]
            #Filter out attributes added at class creation.
            if callable(generic):
                try:
                    #Warning: possiblity of Metaclass giving falses?
                    getattr(cls, name)
                except AttributeError:
                    setattr(cls, name, generic)

    #Properties.
    def __get_node(cls):
        return cls.__node

    Node = property(__get_node,
                    doc = "The Node class of the tree class object.")

    def __repr__(cls):
        return "%s<Node:%r>" % (cls.__name__,
                                cls.Node)

    def clone(cls, name, node):
        """Return a clone *child* class with a different Node class."""
        bases, dct = (cls,), {'Node':node}
        return cls.__class__(name, bases, dct)


#Object to tackle default arguments.
_NullArg = []


class MutableTree(object):
    """The generalized MutableTree tree class.

    Minimal protocol description of tree classes:
    Two attributes: cargo, subtrees. The subtrees attribute returns an
    iterable over the subtrees of the tree.

    If the tree is empty, fetching its cargo raises TypeError.

    In the current implementation you can rebind subtrees or delete it
    altogether. You can also do completely foolish things like adding
    garbage to it. To prevent these things just write an apropriate
    node class and/or a subtrees descriptor. Or pay attention to what
    you are doing."""

    __metaclass__ = MetaTree

    def __init__(self, cargo = _NullArg, *subtrees):
        """The initializer."""
        super(MutableTree, self).__init__(cargo, *subtrees)
        if cargo is not _NullArg:
            self.__cargo = cargo
            self.subtrees = self.__class__.Node(subtrees)
        else:
            self.subtrees = self.__class__.Node(())

    #Properties.
    def __get_cargo(self):
        try:
            return self.__cargo
        except AttributeError:
            #Instead of AttributeError, as in earlier recipe, we
            #raise TypeError - makes much more sense.
            raise TypeError("Cannot fetch cargo of empty tree.")

    def __set_cargo(self, cargo):
        self.__cargo = cargo

    cargo = property(__get_cargo,
                     __set_cargo,
                     doc = "The cargo (top node) of the tree.")

    def __nonzero__(self):
        """Return True if it is the empty Tree, False otherwise."""
        try:
            self.cargo
        except TypeError:
            return False
        else:
            return True

    def __repr__(self):
        if self:
            if self.isAtom():
                ret = "%s" % self.cargo
            else:
                contents = [repr(subtree) for subtree in self.subtrees]
                ret = "%s, %s" % (self.cargo, ", ".join(contents))
        else:
            ret = ''
        return "%s<%s>" % (self.__class__.__name__,
                           ret)

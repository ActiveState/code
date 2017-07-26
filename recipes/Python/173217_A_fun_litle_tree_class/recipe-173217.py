## for python 2.2+
from __future__ import generators
__version__ = '1.0.12'

#--------------------------------------------------------------CTree---
class CTree:
    '''Generate a Class Tree.
    
    Tree characteristics and restrictions:
        - all children of any single node must have unique names.
        - the tree nodes are sorted in order of definition.
        - due to the fact that  in standard python the recursion depth 
          is limited (1000  by default) this tree can  not exceed this 
          limit.                                                       
        - all node names must comply  with identifier naming rules for
          the python language (i.e. [_a-zA-Z][_0-9a-zA-Z]*).
    the interface is as follows:
        - on init the path is a dot separated branch to be created.
        - on call if the path exists return the last mentioned element 
          else create the part that does not exist and return the last 
          element.                                                     
    '''
    def __init__(self, path='', separator='.'):
        '''
        Generate a tree branch corresponding to the path given.

        path      : a <separator> delimited path to be created.
        separator : the path delimiter ('.' by default)
        '''
        self.__leafs = '_' + self.__class__.__name__ + '__leafs' in self.__dict__ and self.__leafs or []
        try:
            c_path = (path.split(separator,1)[0], path.split(separator,1)[1])
            if not c_path[0] in self.__dict__:
                # generate the tail of the branch
                setattr(self, c_path[0], self.__class__(c_path[1], separator))
                self.__leafs.append(self.__dict__[c_path[0]])
            else:
                # go down one level
                getattr(self, c_path[0]).__init__(c_path[1], separator) 
        except IndexError:
            # do this if we are at the end of the path/branch
            c_path = path.split(separator,1)[0]
            path != '' and not c_path in self.__dict__ and \
                not self.__dict__.update({c_path: self.__class__()}) and \
                    not self.__leafs.append(self.__dict__[c_path])
    # this acts as a proxy to __init__
    def __call__(self, path='', separator='.'):
        '''
        Generate a tree branch corresponding to the path given.

        path      : a <separator> delimited path to be created.
        separator : the path delimiter ('.' by default)
        '''
        self.__init__(path, separator)
        return eval('self' + (path!='' and '.' + (separator != '.' and path.replace(separator,'.') or path) or ''))
    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
                len(self.__leafs) == len(other.__leafs) and \
                    not ( 0 in [ l0 == l1 for l0, l1 in zip(self.__leafs, other.__leafs) ] )
    def __ne__(self, other):
        return not (self == other)
    def __iter__(self, func=lambda lst, tail: lst + tail):
        '''
        this generator  will iterate  through the tree  (left-to-right
        depth-first).
        func : a function taking two parameters, the first is the list
               of sub-nodes  of the  current node,  the second  is the 
               stack representing the tail  of the returning node list 
               (excluding  the   returned  nodes).   And  returning  a 
               combined list of nodes.
        '''
        node_list = [self]
        while 1:
            try:
                cur = node_list.pop(0)
                node_list = func(cur.__leafs, node_list)
                yield cur
            except AttributeError:
                yield cur
            except IndexError:
                return
    def flat_iter(self):
        '''
        left-to-right breadth-first generator.
        '''
        return self.__iter__(lambda lst, tail: tail + lst)
    def __delattr__(self, name):
        try:
            self.__dict__[name] in self.__leafs and self.__leafs.remove(self.__dict__[name])
            del self.__dict__[name]
        except KeyError:
            raise AttributeError

#----------------------------------------------------------------------

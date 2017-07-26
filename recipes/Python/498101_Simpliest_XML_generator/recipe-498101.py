__name__        = 'xmlfetch.py'
__author__      = 'Trionice'
__date__        = '9-11-2006'
__version__     = '0.1.1'
__license__     = 'GPL'
__copyright__   = 'Copyright (c) Ivan Furone, 2006'


__all__ = ['xmlfetch','operator','repr','types']
filter(__import__, __all__)



class XMLObj(object):

    tree = str()

    def __init__(self,tree=''):

        self.tree = tree + XMLObj.tree
        return self.tree

class XMLFetch(XMLObj):

     def __init__(self, version=1.0, charset="UTF-8", standalone="yes"):
         self.version =     version
         self.charset =     charset
         self.standalone =  standalone

         self.tree = XMLObj.__init__(self,tree=XMLObj.tree)
         self.nodes = ()

     def _gendecl(self):

        """
        Returns a string representing a standard XML 1.0 declaration equal
        as it is default initialized in __init__.

        """

        return '<? xml version="%f" charset="%s" standalone="%s"?>' \
    % (self.version,self.charset,self.standalone)

     def _embedparser(self, tree, XMLparser='xml.sax'):

         """
         Returns a correctly parsed chunk of valid xml according to the parsing
         libraries it relies on (currently it relies on xml.sax only)

         """

         from xml.sax.handler import ContentHandler
         if XMLparser == 'xml.sax':import xml.sax
         pstring = tree;TempHandler = ContentHandler()
         try:
            do_parse = xml.sax.parseString(pstring,TempHandler)
         except:
            return False
         return True

     def _is_node(self, node):

        """
        Checks if a given node is present in the class dict that holds the nodes for
        further processing.

        """

        is_node = node in self.__dict__[nodes]
        if is_node:
            flag = True
        return flag

     def _diffnode(self, node):

        """
        Find equivalence between two nodes.

        """

        if map (self._is_node,(nodeA, nodeB))[0] == True:
            diff = cmp(self, nodeA, nodeB)
            if diff == 0:
                return nodeA
            else: return None

     def yieldattr(self, attr):


        """
         Takes as argument a dictionary which keys are the names of a node's
         attributes,each one bound with their value.It processes the dict's items,
         returning a string from the resulting list of just-unpacked tuples.

        """
        t = attr.items()
        t2 = []
        for item in t[:]:
            t2.append(' %s = "%s" ' %(item[0],item[1]))
            if not item:
                break
                try :
                    return ''
                except :
                    pass
            else :
                continue
        return str(t2).lstrip("['").rstrip("']").replace("'","").replace(",","")

     def buildnode(self, nodename, splitargs, attrib={}, content=''):

        """
        Takes a node's name,attributes and content - a string,a mapping and another
        string respectively - and returns an XML node crafted accordingly with
        the parameters aforementioned.

        nodename is the node's name expressed as a string;splitargs is a boolean
        which when set to zero returns the node as a whole element,and when set to
        1 will return each one separately inspite.

        """
        
        node1 = '<' + nodename + self.yieldattr(attrib) + '>'
        node2 = '</' + nodename + '>'
        if splitargs == 0:
            node = node1 + content + node2
            return node
        else:
            return node1,content,node2

     def enclosenode(self, parent, node, pcontent='',ncontent='',\
      pattrib=None, nattrib=None):

        """
        Takes as arguments the name of a parent node,that of a child one,their
        attributes and contents respectively expressed;returns a new entity formed
        by the two nodes - in other words the child folded in the parent.
        Wrapper around buildnode

        """

        tmparent = parent
        tmpnode = node
        tmparent = self.buildnode(parent,1,attrib = pattrib,content = pcontent)
        tmpnode = self.buildnode(node,0,attrib = nattrib, content = ncontent)
        node = tmparent[0] + pcontent + tmpnode + tmparent[2]
        return node

     def buildcdata(self, text):

        """
        Returns a CDATA section out of a string.

        """

        cdata = text
        return '<!CDATA[' + cdata + ']]>'

     def buildcomment(self, text, center=0):

        """
        Returns a comment out of a string.

        """

        comment = text
        return '<!--' + comment + '-->'


     def appendnode(self, node, tree):
         """
         Appends a node - without interpolation - to the XMLFetch's classdict
         returns True if the node has been inserted,and ValueError if it is not.
         (This happens usually if the mapping that holds the nodes itself has been
         altered to be read-only.)

         """

         if node is not StringTypes:
            tmpnode = str(node)
            node = tmpnode
         else :
              pass
         self.__dict__[nodes].append(node)
         return node in self.__dict__[nodes]

     def getnodesfromdict(self):

         """
         Acquires the node list from self.__dict__ .

         """

         nodelist = []
         for node in self.__dict__[nodes]:
            nodelist.append(node)
            return nodelist

     def composeXML(self, tree, add_decl=1):

        """
        Retrieves a XML tree previously defined elsewhere and declaration is added
        if add_decl is 1.

        """

        worktree = tree
        tmptree = str(getnodes())
        if add_decl == 0:
            decl = self._gendecl()
            tree = decl + tmptree
        else: tree = worktree
        return tree


     def XMLtoFileObject(self, fname, tree=None):

        """
        Gets as arguments a filename and a tree then writes the tree to a file with
        the given filename.Returns true if everything has been accomplished
        correctly.A IO error is also raised in the bad case.

        """

        try :
            import os.path
            xmlworktree = tree
            if os.path.exists(fname):
                xmlobj = file(fname,mode='ab+')
            else:
                xmlobj = file(fname,mode='wb+')
            xmlobj.write(xmlworktree)
            xmlobj.close()
            return True
        except ImportError:
            raise ImportError, "os.path missing or behaving uncorrectly.Review your \
        Python's version notes"

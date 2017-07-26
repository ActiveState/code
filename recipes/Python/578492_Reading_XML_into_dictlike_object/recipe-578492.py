"""
Module: xml2dict

Author: Lucas Oliveira
Version: 1.0
Website: https://bitbucket.org/luk51000/xml2dict
"""

import lxml
import lxml.etree as et

__author__ = "Lucas Oliveira <luk51000 at gmail dot com>"
__date__  = "13 March 2013"

"""
TODO Set attributes using __setattr__. Tried modifying <http://code.activestate.com/recipes/389916-example-setattr-getattr-overloading/> but it didn't work.
    def __setattr__(self, name, value):
        #Maps attributes to values.
        #Only if we are initialised
        #Source: http://code.activestate.com/recipes/389916-example-setattr-getattr-overloading/

        if not self.__dict__.has_key('_XML__initialised'):  # this test allows attributes to be set in the __init__ method
            return object.__setattr__(self, name, value)
        elif self.__dict__.has_key(name):       # any normal attributes are handled normally
            object.__setattr__(self, name, value)
        else:
            self.__setitem__(name, value)
TODO Allow creation and modification of XML files through same class/instance.
"""

class xml2dict(object):
    def __init__(self, *a, **k):
        # Importing names from *a and **k or using defaults
        self.ffpath = k.setdefault('ffpath', None)
        self.root   = k.setdefault('root', None) if 'tree' not in k else k['tree'].getroot()

        if len(a) > 0:
            etype   = type(et.Element("a"))
            ettype  = type(et.ElementTree())
            for s in a:
                if isinstance(s, (etype,ettype)):
                    if self.root == None:
                        self.root = s.getroot() if isinstance(s,ettype) else s
                elif isinstance(s, str):
                    if self.ffpath == None:
                        self.ffpath = s
                else:
                    raise ValueError("XML\'s initializer only accepts string, ElementTree or Element")
        
        if self.ffpath != None and self.root == None:
            try:
                self.root = et.parse(self.ffpath).getroot()
            except (IOError, et.ParseError):
                # TODO Populate tree and save it
                raise
    def __getitem__(self, key):
        if len(self.root) == 0:
            raise KeyError("Key \'%s\' not found on path \'%s\'" % (str(key),self.root))
        else:
            item = None
            k = str(key)
            for child in self.root:
                if child.tag == k:
                    if item != None:
                        raise KeyError("Key \'%s\' found multiple times on path \'%s\'. Check XML writing module for errors." % (str(key),self.tree.getpath(self.root)))
                    item = child
                        
            if item == None:
                raise KeyError("Key \'%s\' not found on file \'%s\'" % (str(key), self.ffpath))
            return xml2dict(item)
    def __getattr__(self, name):
        try:
            attr = self.root.text if name == 'text' else self.root.get(name)
        finally:
            if attr == None:
                raise AttributeError("Could not find \'%s\'" % name)
            return attr

    # Auxiliar Functions
    def __str__(self):
        return et.tostring(self.root, pretty_print=True, with_tail=False).strip()
    def __len__(self):
        return len(self.root)
    def __dir__(self):
        return list(self.root)
    def __iter__(self):
        for child in self.root:
            yield child.tag
    def __contains__(self,item):
        i = str(item)
        for child in self.root:
            if child.tag == item:
                return True
        return False

if __name__ == "__main__":
    a = XML('file.xml')
    print a['parent1']
    print a['parent1']['child1']
    print a['parent2'].name_of_attribute
    print a['parent3'].text

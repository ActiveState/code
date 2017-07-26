import ast, re, sys
from xml.dom import minidom

try:
    from xml.etree import cElementTree as etree
except:
    try:
        from lxml import etree
    except:
        from xml.etree import ElementTree as etree

def prettify(xml_string):
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="  ") 

class ast2xml(ast.NodeVisitor):
    def __init__(self):
        super(ast.NodeVisitor, self).__init__()
        self.path = []
        self.root = etree.Element('ast')
        self.celement = self.root
        self.lname = 'module'
    def convert(self, tree):
        self.visit(tree)
        return etree.tostring(self.root)
    def generic_visit(self, node):
        self.path.append(type(node).__name__)
        ocelement = self.celement
        self.celement = etree.SubElement(self.celement, self.lname)
        self.celement.attrib.update({'_name': type(node).__name__})
        olname = self.lname
        self.lname = type(node).__name__
        for item in node.__dict__:
            self.lname = item
            if isinstance(getattr(node, item), ast.AST):
                self.generic_visit(getattr(node, item))
            elif isinstance(getattr(node, item), list):
                ocel2 = self.celement
                olname2 = self.lname
                self.celement = etree.SubElement(self.celement, self.lname)
                self.celement.attrib.update({'_name': '_list'})
                self.lname = '_list_element'
                [self.generic_visit(childnode) for childnode in getattr(node, item) if isinstance(childnode, (ast.AST, list))]
                self.celement = ocel2
                self.lname = olname2
            else:
                self.celement.attrib.update({item: str(getattr(node, item))})
        self.path.pop()
        self.celement = ocelement
        self.lname = olname

def main(fpath):
    with open(fpath, 'r') as f:
        tree = ast.parse(f.read())
        res = ast2xml().convert(tree)
        print prettify(res)

if __name__ == '__main__':
    main(sys.argv[1])

from xml.dom.minidom import Document, parse, parseString
from types import StringType, UnicodeType
import string

enc = "iso-8859-1"

def _encode(v):
    if isinstance(v, UnicodeType):
        v = v.encode(enc)
    return v

class XMLElement:

    def __init__(self, doc, el):
        self.doc = doc
        self.el = el

    def __getitem__(self, name):
        a = self.el.getAttributeNode(name)
        if a:
            return _encode(a.value)
        return None

    def __setitem__(self, name, value):
        self.el.setAttribute(name, _encode(value))

    def __delitem__(self, name):
        self.el.removeAttribute(name)

    def __str__(self):
        return _encode(self.doc.toprettyxml())

    def toString(self):
        return _encode(self.doc.toxml())

    def _inst(self, el):
        return XMLElement(self.doc, el)

    def get(self, name, default=None):
        a = self.el.getAttributeNode(name)
        if a:
            return _encode(a.value)
        return _encode(default)

    def add(self, tag, **kwargs):
        el = self.doc.createElement(tag)
        for k, v in kwargs.items():
            el.setAttribute(k, _encode(str(v)))
        return self._inst(self.el.appendChild(el))

    def addText(self, data):
        return self._inst(
            self.el.appendChild(
                self.doc.createTextNode(_encode(data))))

    def addComment(self, data):
        return self._inst(
            self.el.appendChild(
                self.doc.createComment(data)))

    def getText(self, sep=" "):
        rc = []
        for node in self.el.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return _encode(string.join(rc, sep))

    def getAll(self, tag):
        return map(self._inst, self.el.getElementsByTagName(tag))

class _Document(Document):

    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write('<?xml version="1.0" encoding="%s" ?>\n' % enc)
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)

class XMLDocument(XMLElement):

    def __init__(self, tag=None, **kwargs):
        self.doc  = _Document()
        XMLElement.__init__(self, self.doc, self.doc)
        if tag:
            self.el = self.add(tag, **kwargs).el

    def parse(self, d):
        self.doc = self.el = parse(d)
        return self

    def parseString(self, d):
        self.doc = self.el = parseString(_encode(d))
        return self

if __name__=="__main__":

    # Example of dumping a database structure
    doc = XMLDocument("database", name="testdb")
    table = doc.add("table", name="test")
    table.add("field", name="counter", type="int")
    table.add("field", name="name", type="varchar")
    table.add("field", name="info", type="text")
    print doc

    # Simulate reading a XML file
    ndoc = XMLDocument()
    ndoc.parseString(str(doc))
    root = ndoc.getAll("database")
    if root:
        db = root[0]
        print "Database:", db["name"]
        for table in db.getAll("table"):
            print "  Table:", table["name"]
            for field in db.getAll("field"):
                print "    Field:", field["name"], "- Type:", field["type"]

    # It's object oriented
    print XMLDocument("notice").add("text",format="plain").addText("Some text")

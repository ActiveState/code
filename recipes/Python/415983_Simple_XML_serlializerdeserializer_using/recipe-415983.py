"""Simple XML marshaling (serializing) and
  unmarshaling(de-serializing) module using Python
  dictionaries and the marshal module.
"""

from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import XMLReader
from xml.sax import make_parser
import marshal
import os,sys,zlib

class XMLDictionaryHandler(ContentHandler):
    """SAX Handler class which converts an XML
    file to a corresponding Python dictionary """

    def __init__(self):
        self.curr=''
        self.parent=''
        self.count=0
        self.d = {}
        self.currd = {}
        self.parentd = {}
        self.stack = []
        self.stack2 = []

    def startElement(self, name, attrs):
        """ Start element handler """

        if self.count==0:
            self.parent=name
            self.d[name] = [dict(attrs),
                            '',
                            []]
            self.currd = self.d
        else:
            chld={name: [dict(attrs),
                         '',
                         [] ]}
            self.parent = self.stack[-1]
            self.parentd = self.stack2[-1]

            chldlist = (self.parentd[self.parent])[2]
            chldlist.append(chld)
            self.currd = chld

        self.stack.append(name)
        self.stack2.append(self.currd)

        self.curr=name
        self.count += 1

    def endElement(self, name):
        """ End element handler """

        self.stack.remove(name)
        for item in self.stack2:
            if item.has_key(name):
                self.stack2.remove(item)

    def characters(self, content):
        """ Character handler """

        content = (content.encode('utf-8')).strip()

        if content:
            myd=((self.parentd[self.parent])[2])[-1]
            currcontent = (myd[self.curr])[1]
            (myd[self.curr])[1] = "".join((currcontent, content))

    def endDocument(self):
        """ End document handler """
        
        # Compress all text items
        self.packtext(self.d)
        
    def packtext(self, map):
    
        for key, value in map.items():
            text = value[1]
            value[1] = zlib.compress(text)
            children = value[2]
            for submap in children:
                self.packtext(submap)
        
class BinXMLSAXParser(XMLReader):
    """A parser for Python binary marshal files representing
    XML information using SAX interfaces """

    def __init__(self):
        XMLReader.__init__(self)
        self.depth = 0

    def parse(self, stream):
        """ Parse Method """

        # Check if it is a file object
        if type(stream) is file:
            try:
                self.d = marshal.load(stream)
            except Exception, e:
                sys.exit(e)

        # Check if it is a file path
        elif os.path.exists(stream):
            try:
                self.d = marshal.load(open(stream,'rb'))
            except Exception, e:
                sys.exit(e)
        else:
            raise 'BinXMLSAXParserException: Invalid Input Source'

        self._cont_handler.startDocument()
        self.__parse(self.d)
        self._cont_handler.endDocument()

    def __parse(self, map):
        """ Recursive parse method for
        XML dictionary """

        for key, value in map.items():
            # For pretty printing
            self._cont_handler.ignorableWhitespace(" "*self.depth)
            attrs = value[0]
            text = value[1]
            children = value[2]
            # Fire startElement handler event for key
            self._cont_handler.startElement(key, attrs)
            # Fire character handler event for value
            self._cont_handler.characters(zlib.decompress(text))
            # Nested element, recursively call
            # this function...
            self.depth += 1
            # For pretty printing
            self._cont_handler.ignorableWhitespace('\n')
            for child in children:
                self.__parse(child)
            self.depth -= 1
            # For pretty printing
            self._cont_handler.ignorableWhitespace(" "*self.depth)
            # Fire end element handler event
            self._cont_handler.endElement(key)
            # For pretty printing
            self._cont_handler.ignorableWhitespace('\n')

class XMLMarshal(object):
    """ The XML marshalling class """

    def dump(stream, xmlfile):
        """ Serialize XML data to a file """

        try:
            p=make_parser()
            h = XMLDictionaryHandler()
            p.setContentHandler(h)
            p.parse(open(xmlfile))
            # print h.d
            marshal.dump(h.d, stream)
        except Exception, e:
            sys.exit(e)

    def dumps(stream, xmlfile):
        """ Serialize XML data to a string """

        try:
            p=make_parser()
            p.setContentHandler()
            h = XMLDictionaryHandler()
            p.parse(open(xmlfile))
            return marshal.dumps(h.d, stream)
        except Exception, e:
            sys.exit(e)

        return None

    def load(stream, out=sys.stdout):
        """ Load an XML binary stream
        and send XML text to the output
        stream 'out' """

        try:
            p=BinXMLSAXParser()
            p.setContentHandler(XMLGenerator(out))
            p.parse(stream)
        except Exception, e:
            sys.exit(e)

    def loads(stream):
        """ Load an XML binary stream
        and return XML text as string """

        import cStringIO
        c=cStringIO.StringIO()

        try:
            p=BinXMLSAXParser()
            p.setContentHandler(XMLGenerator(c))
            p.parse(stream)
        except Exception, e:
            sys.exit(e)

        return c.getvalue()

    dump=staticmethod(dump)
    dumps=staticmethod(dumps)
    load=staticmethod(load)
    loads=staticmethod(loads)

if __name__ == '__main__':

    fname = 'sample.xml'
    binname = os.path.splitext(fname)[0] + '.bin'

    # Dump XML text to binary
    XMLMarshal.dump(open(binname,'wb'), fname)
    # Dump XML binary to text
    XMLMarshal.load(open(binname,'rb'), open('sample.xml','w'))

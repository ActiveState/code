"""
This module monkey patches the ElementTree module to fully support CDATA
sections both while generating XML trees and while parsing XML documents.

See usage examples at the end of this file.

Eli Golovinsky, 2008
www.gooli.org
"""

try:
    # Try Python 2.5 and later
    import xml.etree.ElementTree as etree
except ImportError:
    # Older Python with ElementTree installed from http://effbot.org/zone/element-index.htm
    import elementtree.ElementTree as etree

def CDATA(text=None):
    """
    A CDATA element factory function that uses the function itself as the tag
    (based on the Comment factory function in the ElementTree implementation).
    """
    element = etree.Element(CDATA)
    element.text = text
    return element

# We're replacing the _write method of the ElementTree class so that it would 
# recognize and correctly print out CDATA sections.
old_ElementTree = etree.ElementTree
class ElementTree_CDATA(old_ElementTree):
    def _write(self, file, node, encoding, namespaces):
        if node.tag is CDATA:
            if node.text:
                text = node.text.encode(encoding)
                file.write("<![CDATA[%s]]>" % text)
        else:
            old_ElementTree._write(self, file, node, encoding, namespaces)
etree.ElementTree = ElementTree_CDATA

# Since xml.parsers.expat supports parsing CDATA sections, all we need to do
# is recognize them during parsing and add them to the tree.
old_XMLTreeBuilder = etree.XMLTreeBuilder
class XMLTreeBuilder_CDATA(old_XMLTreeBuilder):
    def __init__(self, html=0, target=None):
        old_XMLTreeBuilder.__init__(self, html, target)
        self._parser.StartCdataSectionHandler = self._start_cdata
        self._parser.EndCdataSectionHandler = self._end_cdata
        self._cdataSection = False
        self._cdataBuffer = None
        
    def _start_cdata(self):
        """
        A CDATA section beginning has been recognized - start collecting
        character data.
        """
        self._cdataSection = True
        self._cdataBuffer = []
        
    def _end_cdata(self):
        """
        The CDATA section has ended - join the character data we collected
        and add a CDATA element to the target tree.
        """
        self._cdataSection = False
        text = self._fixtext("".join(self._cdataBuffer))
        self._target.start(CDATA, {})
        self._target.data(text)
        self._target.end(CDATA)
        
    def _data(self, text):
        """
        If we are in the middle of a CDATA section, collect the data into a
        special buffer, otherwise treat it as before.
        """
        if self._cdataSection:
            self._cdataBuffer.append(text)
        else:
            old_XMLTreeBuilder._data(self, text)

etree.XMLTreeBuilder = XMLTreeBuilder_CDATA

try:
    # Try Python 2.5 and later
    from xml.etree.ElementTree import *
except ImportError:
    # Older Python with ElementTree installed from http://effbot.org/zone/element-index.htm
    from elementtree.ElementTree import *

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    sampleXml = '<data key="value"> some text <![CDATA[<sender>John Smith</sender>]]></data>'

    # Parse XML that contains CDATA sections and convert it back into a string
    root = fromstring(sampleXml)
    xml = tostring(root)
    print xml
    
    # The parsed and regenerated XML is the same as the sample XML string
    assert(sampleXml == xml) 
    
    # Generate a tree with a CDATA section
    root = Element("data")
    root.set("key", "value")
    root.text = " some text "
    cdata = CDATA("<sender>John Smith</sender>")
    root.append(cdata)
    xml2 = tostring(root)
    print xml2

    # The generated XML is the same as the sample XML string
    assert(sampleXml == xml2) 

from xml.dom import minidom

class XmlNode:
    """An XML node represents a single field in an XML document."""

    def __init__(self, domElement):
        """Construct an XML node from a DOM element."""
        self.elem = domElement
    
    @classmethod
    def makeRoot(cls, xmlFileName):
        return cls(minidom.parse(xmlFileName))

    def getData(self):
        """Extract data from a DOM node."""
        for child in self.elem.childNodes:
            if child.nodeType == child.TEXT_NODE:
                return str(child.data)
        return None

    def getAttributeValue(self, name):
        """Returns the value of the attribute having the specified name."""
        return str(self.elem.attributes[name].value)

    def getChild(self, tag):
        """Returns the first child node having the specified tag."""
        return XmlNode(self.elem.getElementsByTagName(tag)[0])
    
    def getChildren(self, tag):
        """Returns a list of child nodes having the specified tag."""
        return [XmlNode(x) for x in self.elem.getElementsByTagName(tag)]

# Import ElementTree according to Fredrik Lundh's own recipe
#   see: http://mail.python.org/pipermail/python-dev/2006-August/068504.html

try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        import elementtree.ElementTree as ET


# Converter

def DOM2ET(domelem):
    """Converts a DOM node object of type element to an ElementTree Element.

    domelem: DOM node object of type element (domelem.nodeType == domelem.ELEMENT_NODE)

    returns an 'equivalent' ElementTree Element
    """
    # make some local variables for fast processing
    tyCDATA = domelem.CDATA_SECTION_NODE
    tyTEXT = domelem.TEXT_NODE
    tyPI = domelem.PROCESSING_INSTRUCTION_NODE
    tyCOMMENT = domelem.COMMENT_NODE
    tyELEMENT = domelem.ELEMENT_NODE
    # calculate the attributes of the domelem
    attribs = domelem.attributes
    attrs = dict((x.name, x.value) for x in (attribs.item(i) for i in range(attribs.length)))
    # build the ET Element
    etelem = ET.Element(domelem.tagName, attrs)
    last = None # to differentiate between 'text' and 'tail'
    for node in domelem.childNodes:
        nodeType = node.nodeType
        if (tyTEXT == nodeType or tyCDATA == nodeType) and node.data:
            data = node.data
            if last is None: etelem.text = etelem.text + data if etelem.text else data
            else: last.tail = last.tail + data if last.tail else data
        elif tyELEMENT == nodeType:
            last = DOM2ET(node)
            etelem.append(last)
        elif tyCOMMENT == nodeType:
            last = ET.Comment(node.data)
            etelem.append(last)
        elif tyPI == nodeType:
            last = ET.ProcessingInstruction(node.target, node.data)
            etelem.append(last)

    return etelem


if __name__ == "__main__":
    import xml.dom.minidom as minidom

    xmltext = '<ELEM key="value">text<SUBELEM/>tail</ELEM>'
    doc = minidom.parseString(xmltext)
    topelem = doc.documentElement
    etelem = DOM2ET(topelem)
    print ET.tostring(etelem) # prints: <ELEM key="value">text<SUBELEM />tail</ELEM>

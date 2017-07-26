## Remove whitespace-only text nodes from an XML DOMOriginally published: 2004-09-02 01:47:21 
Last updated: 2004-09-13 16:00:48 
Author: Brian Quinlan 
 
XML parsers consider several conditions when deciding which whitespace-only text nodes should be preserved during DOM construction. Unfortunately, those conditions are controlled by the document's DTD or by the content of document itself. Since it is often difficult to modify the DTD or the XML, this recipe simple removes all whitespace-only text nodes from a DOM node.
"""
Using the Apache XPath API from Jython
Based on the the ApplyXPath.java example in the xalan distribution.

Sean McGrath
"""

import sys
import java

from javax.xml.parsers import DocumentBuilderFactory
from java.io import FileInputStream
from java.io import OutputStreamWriter

from org.apache.xpath import XPathAPI
from org.w3c.dom import Document
from org.w3c.dom import Node
from org.w3c.dom.traversal import NodeIterator
from org.xml.sax import InputSource

from javax.xml.transform import Transformer, OutputKeys, TransformerFactory
from javax.xml.transform.dom import DOMSource
from javax.xml.transform.stream import StreamResult

def DoXPath (Filename,XPathString):
	IS = InputSource (FileInputStream (Filename))
	df = DocumentBuilderFactory.newInstance()
	df.setNamespaceAware(1)
	doc = df.newDocumentBuilder().parse(IS)
	serializer = TransformerFactory.newInstance().newTransformer()
	serializer.setOutputProperty (OutputKeys.OMIT_XML_DECLARATION, "yes")
	nl = XPathAPI.selectNodeIterator (doc,XPathString)
	n = nl.nextNode()
	while n:
		if IsTextNode (n):
			# Coalesce contiguous text nodes
			res = [n.getNodeValue()]
			nn = n.getNextSibling()
			while (nn):
				res.append (nn.getNodeValue())
				nn = n.getNextSibling()
			java.lang.System.out (string.join(res,""))
		else:
			serializer.transform (DOMSource(n), StreamResult (OutputStreamWriter (java.lang.System.out)))
		java.lang.System.out.println()
		n = nl.nextNode()

def IsTextNode(n):
	return (n.getNodeType() in [Node.TEXT_NODE,Node.CDATA_SECTION_NODE])

if __name__ == "__main__":
	if len (sys.argv) != 3:
		sys.stderr.write ("Usage: %s filename xpath\n" % sys.argv[0])
	else:
		DoXPath (sys.argv[1],sys.argv[2])

==================================================
xmlreader.py:
==================================================
from xml.dom.minidom import parse


class NotTextNodeError:
    pass


def getTextFromNode(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    t = ""
    for n in node.childNodes:
	if n.nodeType == n.TEXT_NODE:
	    t += n.nodeValue
	else:
	    raise NotTextNodeError
    return t


def nodeToDic(node):
    """
    nodeToDic() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
	- if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
	- if the node has the attribute "method" set to "true",
    then it's children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
	- else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary).
    """
    dic = {} 
    for n in node.childNodes:
	if n.nodeType != n.ELEMENT_NODE:
	    continue
	if n.getAttribute("multiple") == "true":
	    # node with multiple children:
	    # put them in a list
	    l = []
	    for c in n.childNodes:
	        if c.nodeType != n.ELEMENT_NODE:
		    continue
		l.append(nodeToDic(c))
	        dic.update({n.nodeName:l})
	    continue
		
	try:
	    text = getTextFromNode(n)
	except NotTextNodeError:
            # 'normal' node
            dic.update({n.nodeName:nodeToDic(n)})
            continue

        # text node
        dic.update({n.nodeName:text})
	continue
    return dic


def readConfig(filename):
    dom = parse(filename)
    return nodeToDic(dom)





def test():
    dic = readConfig("sample.xml")
    
    print dic["Config"]["Name"]
    print
    for item in dic["Config"]["Items"]:
	print "Item's Name:", item["Name"]
	print "Item's Value:", item["Value"]

test()



==================================================
sample.xml:
==================================================
<?xml version="1.0" encoding="UTF-8"?>

<Config>
    <Name>My Config File</Name>
    
    <Items multiple="true">
	<Item>
	    <Name>First Item</Name>
	    <Value>Value 1</Value>
	</Item>
	<Item>
	    <Name>Second Item</Name>
	    <Value>Value 2</Value>
	</Item>
    </Items>

</Config>



==================================================
output:
==================================================
My Config File

Item's Name: First Item
Item's Value: Value 1
Item's Name: Second Item
Item's Value: Value 2

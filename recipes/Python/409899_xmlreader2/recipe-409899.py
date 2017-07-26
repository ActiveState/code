"""
==================================================
xmlreader2.py:
Modified from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/116539
contributed by Christoph Dietze.

Modified to allow it to work with repeating elements without having to specify the multiple attribute.
==================================================
"""
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
    - if there is more than one child with the same name
    then these children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
    - else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary).
    """
    dic = {} 
    multlist = {} # holds temporary lists where there are multiple children
    for n in node.childNodes:
        multiple = False 
        if n.nodeType != n.ELEMENT_NODE:
            continue
        # find out if there are multiple records    
        if len(node.getElementsByTagName(n.nodeName)) > 1:
            multiple = True 
            # and set up the list to hold the values
            if not multlist.has_key(n.nodeName):
                multlist[n.nodeName] = []
        
        try:
            #text node
            text = getTextFromNode(n)
        except NotTextNodeError:
            if multiple:
                # append to our list
                multlist[n.nodeName].append(nodeToDic(n))
                dic.update({n.nodeName:multlist[n.nodeName]})
                continue
            else: 
                # 'normal' node
                dic.update({n.nodeName:nodeToDic(n)})
                continue

        # text node
        if multiple:
            multlist[n.nodeName].append(text)
            dic.update({n.nodeName:multlist[n.nodeName]})
        else:
            dic.update({n.nodeName:text})
    return dic


def readConfig(filename):
    dom = parse(filename)
    return nodeToDic(dom)





def test():
    dic = readConfig("sample.xml")
    
    print dic["Config"]["Name"]
    print
    print "Item Type:", dic["Config"]["Items"]["Type"]
    for item in dic["Config"]["Items"]["Item"]:
        print "Item's Name:", item["Name"]
        print "Item's Value:", item["Value"]
    
    """
    ==================================================
    sample.xml:
    ==================================================
    <?xml version="1.0" encoding="UTF-8"?>

    <Config>
        <Name>My Config File</Name>

        <Items>
            <Type>Item type</Type>
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
    [u'My Config File']

    Item Type: Item type
    Item's Name: First Item
    Item's Value: Value 1
    Item's Name: Second Item
    Item's Value: Value 2
    """
        

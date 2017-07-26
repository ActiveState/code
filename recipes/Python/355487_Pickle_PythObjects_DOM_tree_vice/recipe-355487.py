import xml.dom.minidom as dom

class PickleMeToXML(object): pass

# helper function

def getType(obj):
    """ generates string representation of class of obj 
        discarding decoration """
    return str(obj.__class__).split("'")[1].split(".")[-1]

_easyToPickle = [ "int", "float", "str" ]

_isCallable = lambda o: hasattr(o, "__call__")

# 
#   pickling 
# 

def _pickleDictItems(root, node, fabric):
    for key, value in root.items():
        tempnode = fabric.createElement("item")
        tempnode.appendChild(pickle(key, fabric, "key"))
        tempnode.appendChild(pickle(value, fabric, "value"))
        node.appendChild(tempnode)

def _pickleListItems(root, node, fabric):
    for idx, obj in enumerate(root):
        tempnode = pickle(obj, fabric, "item")
        tempnode.attributes["index"] = str(idx)
        node.appendChild(tempnode)

_pickleTupleItems = _pickleListItems

def pickle(root, fabric, elementName="root"):

    node = fabric.createElement(elementName)
    typeStr = getType(root)
    node.attributes["type"]=typeStr

    if isinstance(root, PickleMeToXML):
        node = _pickleObjectWithAttributes(node, root, fabric, elementName)
    elif typeStr in _easyToPickle:
        node.appendChild(fabric.createTextNode(str(root)))
    elif isinstance(root, dict):
        _pickleDictItems(root, node, fabric)
    elif isinstance(root, list):
        _pickleListItems(root, node, fabric)
    elif isinstance(root, tuple):
        _pickleTupleItems(root, node, fabric)
    else:
        # fallback handler
        node.appendChild(fabric.createTextNode(repr(root)))
    return node

def _pickleObjectWithAttributes(node, root, fabric, elementName):

    # pickle all members or just a subset ??? 
    if hasattr(root, "__pickle_to_xml__"):
        attributesToPickle = root.__pickle_to_xml__
    else:
        # avoid members which are python internal
        attributesToPickle = [ name for name in dir(root) if not name.startswith("__") ]

    for name in attributesToPickle: 
        obj = getattr(root, name)

        # do not pickle member functions
        if _isCallable(obj): continue

        # is there some special encoding method ??
        if hasattr(root, "_xml_encode_%s" % name):
            value = getattr(root, "_xml_encode_%s" % name)()
            node.appendChild(fabric.createTextNode(value))
        else:
            node.appendChild(pickle(obj, fabric, name))
    return node

#
#   unpickling 
#

# helper functions

def _getElementChilds(node, doLower = 1):
    """ returns list of (tagname, element) for all element childs of node """

    dolow = doLower and (lambda x:x.lower()) or (lambda x:x)
    return [ (dolow(no.tagName), no) for no in node.childNodes if no.nodeType != no.TEXT_NODE ]

def _getText(nodelist):
    """ returns collected and stripped text of textnodes among nodes in nodelist """
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc.strip()

# main unpickle function

def unpickle(node):

    typeName= node.attributes["type"].value

    if typeName in _easyToPickle: 
        initValue = _getText(node.childNodes)
        value = eval("%s(%r)" % (typeName, initValue))
        return value 
    elif typeName=="tuple":
        return _unpickleTuple(node)
    elif typeName=="list":
        return _unpickleList(node)
    elif typeName=="dict":
        return _unpickleDict(node)
    else:
        obj = eval("object.__new__(%s)" % typeName)
        for name, element in _getElementChilds(node):
            setattr(obj, name, unpickle(element))
        return obj
        
class XMLUnpicklingException(Exception): pass

def _unpickleList(node):
    li = []
    # collect entries, you can not assume that the
    # members of the list appear in the right order !
    for name, element in _getElementChilds(node):
        if name != "item":
            raise XMLUnpicklingException()
        idx = int(element.attributes["index"].value)
        obj = unpickle(element)
        li.append((idx, obj))

    # rebuild list with right order
    li.sort()
    return [ item[1] for item in li ]

def _unpickleTuple(node):
    return tuple(_unpickleList(node))

def _unpickleDict(node):
    dd = dict()
    for name, element in _getElementChilds(node):
        if name != "item":
            raise XMLUnpicklingException()
        childList = _getElementChilds(element)
        if len(childList) != 2:
            raise XMLUnpicklingException()
        for name, element in childList:
            if name=="key":
                key = unpickle(element)
            elif name=="value":
                value = unpickle(element)
        dd[key]=value
    return dd

if __name__=="__main__":

    # build some nested data structures for testing purposes

    class RootObject(PickleMeToXML):

        counter = 3
        def __init__(self):
            self.sub = SubObject()
            self.data = dict(xyz=4711)
            self.objlist = [ 1, 2, SubObject(), DetailObject() ]

    class SubObject(PickleMeToXML):

        __pickle_to_xml__ = ["values", "detail"]

        def __init__(self):
            self.values = (3.12, 4711, 8.15)
            self.z = "uwe"
            self.detail = DetailObject()

    class DetailObject(PickleMeToXML):

        statement = "1 < 2 is true"
        blablaliste = ["a", "b", "c"]

        def _xml_encode_statement(self):
            # encrypt attribute 'statement'
            return self.statement[::-1]

        def _xml_decode_statement(self, value):
            # decrypt value
            self.statement = value[::-1]

    # testing procedure:
    # convert objects -> xml -> objects -> xml

    obj = RootObject()
    node =pickle(root=obj, fabric=dom.Document())
    x= unpickle(node)
    node = pickle(root = x, fabric=dom.Document())

    # that is how the xml document looks like:
    print node.toprettyxml()

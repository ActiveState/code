from xml.dom import minidom

if not hasattr( minidom.NamedNodeMap, '__contains__' ):
    minidom.NamedNodeMap.__contains__ = minidom.NamedNodeMap.has_key

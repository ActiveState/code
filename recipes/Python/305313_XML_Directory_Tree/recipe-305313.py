import os, os.path
from xml.dom.minidom import Document

doc = Document()

def makenode(path):
    "Return a document node contains a directory tree for the path."
    node = doc.createElement('dir')
    node.setAttribute('name', path)
    for f in os.listdir(path):
        fullname = os.path.join(path, f)
        if os.path.isdir(fullname):
            elem = makenode(fullname)
        else:
            elem = doc.createElement('file')
            elem.setAttribute('name', f)
        node.appendChild(elem)
    return node

doc.appendChild(makenode('/pydev/scheme'))
print doc.toprettyxml()

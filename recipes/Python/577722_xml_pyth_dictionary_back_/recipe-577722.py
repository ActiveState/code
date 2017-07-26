# Create python xml structures compatible with
# http://search.cpan.org/~grantm/XML-Simple-2.18/lib/XML/Simple.pm

from lxml import etree
from itertools import groupby

def xml2d(e):
    """Convert an etree into a dict structure

    @type  e: etree.Element
    @param e: the root of the tree
    @return: The dictionary representation of the XML tree
    """
    def _xml2d(e):
        kids = dict(e.attrib)
        if e.text:
            kids['__text__'] = e.text
        if e.tail:
            kids['__tail__'] = e.tail
        for k, g in groupby(e, lambda x: x.tag):
            g = [ _xml2d(x) for x in g ] 
            kids[k]=  g
        return kids
    return { e.tag : _xml2d(e) }


def d2xml(d):
    """convert dict to xml

       1. The top level d must contain a single entry i.e. the root element
       2.  Keys of the dictionary become sublements or attributes
       3.  If a value is a simple string, then the key is an attribute
       4.  if a value is dict then, then key is a subelement
       5.  if a value is list, then key is a set of sublements

       a  = { 'module' : {'tag' : [ { 'name': 'a', 'value': 'b'},
                                    { 'name': 'c', 'value': 'd'},
                                 ],
                          'gobject' : { 'name': 'g', 'type':'xx' },
                          'uri' : 'test',
                       }
           }
    >>> d2xml(a)
    <module uri="test">
       <gobject type="xx" name="g"/>
       <tag name="a" value="b"/>
       <tag name="c" value="d"/>
    </module>

    @type  d: dict 
    @param d: A dictionary formatted as an XML document
    @return:  A etree Root element
    """
    def _d2xml(d, p):
        for k,v in d.items():
            if isinstance(v,dict):
                node = etree.SubElement(p, k)
                _d2xml(v, node)
            elif isinstance(v,list):
                for item in v:
                    node = etree.SubElement(p, k)
                    _d2xml(item, node)
            elif k == "__text__":
                    p.text = v
            elif k == "__tail__":
                    p.tail = v
            else:
                p.set(k, v)

    k,v = d.items()[0]
    node = etree.Element(k)
    _d2xml(v, node)
    return node
    
    

if __name__=="__main__":

    X = """<T uri="boo"><a n="1"/><a n="2"/><b n="3"><c x="y"/></b></T>"""
    print X
    Y = xml2d(etree.XML(X))
    print Y
    Z = etree.tostring (d2xml(Y) )
    print Z
    assert X == Z

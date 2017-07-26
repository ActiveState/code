"""
MicroXml provides stand-alone support for the basic, most-used features
of XML -- tags, attributes, and element values. That's all. It produces
a DOM tree of XML nodes. It's compatible with Python 2.7 and Python 3.

MicroXml does not support DTDs, CDATAs and other advanced XML features. 
It stores the XML declaration but doesn't use it.

However, within these limitations, MicroXml is easy to use and allows 
far simpler debugging of XML results than when using a full-featured 
XML library. With XmlDoc::to_string() one can round-trip the XML for 
eyeball checking.

It also includes a minimal XPath-like implementation called MicroPath 
for accessing specific XML nodes in the tree. 

Jack Trainor 2015
"""
import sys
        
########################################################################
class MicroPath(object):
    """
    MicroPath locates the first XmlNode matching path specification.

    MicroPath format is quasi-http: "tag1/tag2?key1="val1"&@="val2".
    If key is "@", value is the content of element.
    
    Single or double-quotes can be used with key-values, but are not
    required.
    """
    def __init__(self):
        pass

    def get_dest_node(self, root, path):
        """ Returns first node that matches path. """
        items = path.split("/")
        return self.get_dest_node_from_items(root, items) 

    def get_dest_node_from_items(self, root, items):
        num_items = len(items)
        if (num_items > 1):
            item = items[0]
            items = items[1:]
            for node in root.children:
                dest_node = self.get_dest_node_from_items(node, items)
                if dest_node:
                    return dest_node
        elif (num_items == 1) and self.match_node_item(root, items[0]):
            return root
        return None
    
    def match_node_item(self, node, item):
        match = False
                       
        micro_path_item = MicroPathItem(item)        
        if node.tag == micro_path_item.tag:
            match = True
            
        if match:
            for key in micro_path_item.attrs.keys():
                if key == "@":
                    node_val = node.text
                else:
                    node_val = node.attrs.get(key, None)
                item_val = micro_path_item.attrs.get(key, None)
                if item_val == None or node_val == None:
                    match = False
                    break
                if item_val != node_val:
                    match = False
                    break

        return match
    
########################################################################
class MicroPathItem(object):
    """
    MicroPathItem parses MicroPath string into tag and attributes. 
    """
    def __init__(self, item):            
        self.tag = ""
        self.attrs = {}
        
        sub_items = item.split("?")
        if sub_items:
            self.tag = sub_items[0]
            if len(sub_items) == 2:
                attr_part = sub_items[1]
                attr_items = attr_part.split("&")
                for attr_item in attr_items:
                    attr_sub_items = attr_item.split("=")
                    if len(attr_sub_items) == 2:
                        key, value = attr_sub_items
                        if len(value):
                            if value[0] == '"' and value[-1] == '"':
                                value = value[1:-1]
                            elif value[0] == "'" and value[-1] == "'":
                                value = value[1:-1]
                        self.attrs[key] = value
                        
        
                        
########################################################################
class XBuffer(object):
    """
    Xbuffer provides basic buffer navigation and character collection
    for lexing and parsing.
    
    Not called Buffer to avoid collisions with built-in Buffer.    
    """""
    def __init__(self, text, index=0):
        self.text = text 
        self.index = index
        self.len = len(text)

    def at_end(self):
        return self.index >= (self.len-1)
        
    def inc_index(self):
        if not self.at_end():
            self.index += 1

    def get_char(self):
        if not self.at_end():
            return self.text[self.index]
        return None
        
    def get_next_char(self):
        self.inc_index()
        return self.get_char()
                
    def get_chars_to_delimiter(self, delimiters, incl_delimiter=False):
        chars = []
        found_delimiter = False
        while not self.at_end() and not found_delimiter:
            c = self.get_char()
            found_delimiter = (c in delimiters)
            if not found_delimiter or (found_delimiter and incl_delimiter):
                chars.append(c)
                self.inc_index()
        chars = "".join(chars)
        return found_delimiter, chars
        
    def skip_space(self):
        while not self.at_end():
            c  = self.get_char()
            if str.isspace(c):
                self.inc_index()
            else:
                break

########################################################################
class XmlNode(object):
    """
    An XmlNode carries the information for an XML tag in an XML tree --
    the tag, attributes, and text value of the element plus children
    nodes, if any.   
    """""
    def __init__(self, tag, attributes=None, parent=None):
        self.tag = tag
        self.text = ""
        self.attrs = {}
        self.children = []
        self.parent = None
        if attributes:
            self.attrs = attributes
        if parent:
            parent.add_child(self)
    
    def __repr__(self):
        return "XmlNode: %s [%s] %s" % (self.tag, self.text, self.attrs)
    
    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def append_text(self, text):
        self.text += text

    def get_path(self):
        path_elems = []
        path_elems.append(self.tag)
        parent = self.parent
        while parent != None:
            path_elems.append(parent.tag)
            parent = parent.parent
        path_elems.reverse()
        path = "/".join(path_elems)
        return path
        
    def to_string(self):
        """" Recursively converts nodes and children to text string. """
        s = attrs = ""
        for item in self.attrs.items():
            if attrs != "":
                attrs += " "
            attrs += '%s="%s"' % (item[0], item[1])
        
        if self.children or self.text or str.isspace(self.text):
            if attrs:
                s += '\n<%s %s>' % (self.tag, attrs) 
            else:
                s += '\n<%s>' % (self.tag) 
                
            s += self.text
            for node in self.children:
                s += node.to_string()
            s += '</%s>\n' % self.tag
        else:
            if attrs:
                attrs = " " + attrs
            s += "<%s%s/>\n" % (self.tag, attrs)
        s = s.replace('\n\n', '\n')
        return s

        
########################################################################
"""
Utils for determining type of XML tag.
"""
NO_TAG = 0
START_TAG = 1
END_TAG = 2
EMPTY_TAG = 2
COMMENT_TAG = 4
DECL_TAG = 5
DOCTYPE_TAG = 6

def is_start_tag(xml): 
    if (len(xml) > 2):
        return (xml[0] == "<" and xml[0:2] != "</" and xml[-2:] != "/>")
    return False

def is_end_tag(xml): 
    if (len(xml) > 3):
        return (xml[0] == "<" and xml[0:2] == "</" and xml[-2:] != "/>")
    return False

def is_empty_tag(xml): 
    if (len(xml) > 3):
        return (xml[0] == "<" and xml[0:2] != "</" and xml[-2:] == "/>")
    return False

def is_comment_tag(xml): 
    if (len(xml) > 3):
        return (xml[0] == "<" and xml[0:4] == "<!--" and xml[-3:] == "-->")
    return False

def is_decl_tag(xml): 
    if (len(xml) > 10):
        return (xml[0] == "<" and xml[0:5] == "<?xml" and xml[-2:] == "?>")
    return False

def is_doctype_tag(xml): 
    if (len(xml) > 10):
        return (xml[0] == "<" and xml[0:9] == "<!DOCTYPE" and xml[-1:] == ">")
    return False

def get_tag_type(xml): 
    if is_decl_tag(xml):
        return DECL_TAG
    elif is_doctype_tag(xml):
        return DOCTYPE_TAG
    elif is_comment_tag(xml):
        return COMMENT_TAG
    elif is_start_tag(xml):
        return START_TAG
    elif is_empty_tag(xml):
        return EMPTY_TAG
    elif is_end_tag(xml):
        return END_TAG
    return NO_TAG

########################################################################
class XmlDocument(object):    
    def __init__(self):
        """
        XmlDoc parses XML into a declaration, if present, and node tree 
        of XML elements.
        """
        self.stack = []
        self.declaration = ""
        self.root = None
        
    def push_node(self, node):
        self.stack.append(node)
        
    def pop_node(self):
        node = self.get_cur_node()
        if node != None:
            self.stack = self.stack[:-1]
        else:
            msg = "XmlDocument::pop_node stack empty."
            self.handle_error(msg)
        return node
        
    def get_cur_node(self):
        node = None
        node_count = len(self.stack)
        if node_count > 0:
            node = self.stack[node_count-1]
        return node
    
    def startElement(self, name, attributes=None):
        node = XmlNode(name, attributes)        
        if self.root == None:
            self.root = node           
        curNode = self.get_cur_node()
        if curNode != None:
            curNode.add_child(node)       
        self.push_node( node )
        
    def characters(self, chars):
        node = self.get_cur_node()
        if node:
            node.append_text(chars)

    def endElement(self, name=""):
        node = self.pop_node()
        if node.tag != name:
            msg = "XmlDocument::end_element: tag [%s] not matching node [%s]" \
                   % (name, node)
            self.handle_error(msg)

    def get_name_attrs_from_tag(self, xml):
        """ Gets name and attributes from start tag xml. """
        name = ""
        attrs = {}
        xml = xml.replace("'", '"')
        xbuf = XBuffer(xml)
        xbuf.inc_index()  # skip past '<'
        xbuf.skip_space()
        found_delimiter, name = xbuf.get_chars_to_delimiter([' ', '/','>'])
        c = xbuf.get_char()
        while True:
            if c == ' ':
                xbuf.skip_space()
                found_delimiter, attr_name = xbuf.get_chars_to_delimiter(['='])
                c = xbuf.get_next_char()
                if c == '"':
                    xbuf.inc_index()
                    found_delimiter, attr_val = xbuf.get_chars_to_delimiter(['"'])
                    c = xbuf.get_char()
                    if c == '"':
                        attrs[attr_name] = attr_val
                        xbuf.inc_index()
                else:
                    msg = "XmlDoc::get_name_attrs_from_tag [%s] reached end of buffer too soon." \
                            % xml
                    self.handle_error(msg)
                c = xbuf.get_char()      
            else:
                break 
    
        return name, attrs    

    def lex(self, xml):
        """ Divide xml into raw items delimited by '<' and '>' pair 
        or not so delimited. """
        xbuf = XBuffer(xml)
        raw_items = []
        while not xbuf.at_end():
            found, chars = xbuf.get_chars_to_delimiter(["<"])
            if found and chars and chars != "\n":
                raw_items.append(chars)
                
            if not xbuf.at_end():
                found, chars = xbuf.get_chars_to_delimiter([">"], True)
                if found and chars:
                    raw_items.append(chars)
        return raw_items
 
    def parse(self, xml, strip_empty_chars=True):
        """ Parse xml source into a root node. """
        xml = xml.strip()
        raw_items = self.lex(xml)
        if raw_items: 
            for item in raw_items:
                tag_type = get_tag_type(item)
                if tag_type == START_TAG:
                    name, attrs = self.get_name_attrs_from_tag(item)
                    self.startElement(name, attrs)
                elif tag_type == END_TAG:
                    name = item[2:-1]
                    self.endElement(name)
                elif tag_type == EMPTY_TAG:
                    name, attrs = self.get_name_attrs_from_tag(item)
                    self.startElement(name, attrs)
                    self.endElement(name)
                elif tag_type == COMMENT_TAG:
                    pass # ignore
                elif tag_type == DECL_TAG:
                    self.declaration = item
                elif tag_type == DOCTYPE_TAG:
                    pass # ignore
                else:
                    if strip_empty_chars == True:
                        item = item.strip()
                    self.characters(item)

        return self.root

    def parse_file(self, path, strip_empty_chars=True):
        xml = open(path, 'r').read()
        return self.parse(xml, strip_empty_chars)

    def to_string(self):
        s = ""
        if self.declaration:
            s = self.declaration
        if self.root:
            s += self.root.to_string()
        return s
    
    def handle_error(self, msg):
        raise RuntimeError(msg)       
    
########################################################################
XML = """
<?xml version="1.0"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications 
      with XML.</description>
   </book>
   <book id="bk102">
      <author>Ralls, Kim</author>
      <title>Midnight Rain</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect battles corporate zombies, 
      an evil sorceress, and her own childhood to become queen 
      of the world.</description>
   </book>
   <book id="bk103">
      <author>Corets, Eva</author>
      <title>Maeve Ascendant</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-11-17</publish_date>
      <description>After the collapse of a nanotechnology 
      society in England, the young survivors lay the 
      foundation for a new society.</description>
   </book>
</catalog>
"""

def test_micropath(root, path):
    micro_path = MicroPath()
    dest_node = micro_path.get_dest_node(root, path)
    sys.stdout.write("Node: %s\n" % dest_node)
    if dest_node:
        dest_node_path = dest_node.get_path()
    sys.stdout.write("Node path: %s\n" % dest_node_path)

def test_xmldoc(xml):
    xml_doc = XmlDocument()
    root = xml_doc.parse(xml)
    sys.stdout.write(xml_doc.to_string())
    test_micropath(root, "catalog/book?id=bk103")
    test_micropath(root, "catalog/book/author?@='Ralls, Kim'")

########################################################################
if __name__ == "__main__":
    test_xmldoc(XML)
    
    

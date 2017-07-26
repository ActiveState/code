import xml.etree.ElementTree as ET
import functools

class XMLMaker(object):
    def __getattr__(self, _name):
        return functools.partial(self.make_node, _name)

    def make_node(self, _name, node, **kwargs):
        node = ET.SubElement(node, _name)
        for (key, value) in kwargs.items():
            if key == 'text':
                node.text = value
            else:
                node.attrib[key] = value
        return node

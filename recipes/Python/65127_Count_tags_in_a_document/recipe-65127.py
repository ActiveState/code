from xml.sax.handler import ContentHandler
import xml.sax
class countHandler(ContentHandler):
    def __init__(self):
        self.tags={}

    def startElement(self, name, attr):
        if not self.tags.has_key(name):
            self.tags[name] = 0
        self.tags[name] += 1

parser = xml.sax.make_parser()
handler = countHandler()
parser.setContentHandler(handler)
parser.parse("test.xml")
print handler.tags

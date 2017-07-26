import sys, string
from xml.sax import saxutils, handler, make_parser
import random

class ContentGenerator(handler.ContentHandler):
    vowels = "aeiouAEIOU"
    len_vowels = len(vowels)
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    len_consonants = len(consonants)
    digits = "1234567890"
    len_digits = len(digits)
        
    def __init__(self, out = sys.stdout):
        handler.ContentHandler.__init__(self)
        self._out = out
        self.convertedEltNames = {}
    
    def _pick(self, source, len_source):
        return source[random.randrange(len_source)]
        
    def _convert(self, c):
        if c in self.vowels:
            return self._pick(self.vowels, self.len_vowels)
        elif c in self.consonants:
            return self._pick(self.consonants, self.len_consonants)
        elif c in self.digits:
            return self._pick(self.digits, self.len_digits)
        else:
            return c
        
    def _replace(self, text):
        return "".join([self._convert(c) for c in text])
        
    def _internName(self, name):
        if name not in self.convertedEltNames:
            self.convertedEltNames[name] = self._replace(name)
        return self.convertedEltNames[name]

    # ContentHandler methods
        
    def startDocument(self):
        self._out.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')

    def startElement(self, name, attrs):
        self._out.write('<' + self._internName(name))
        for (name, value) in attrs.items():
            self._out.write(' %s="%s"' % (self._internName(name), saxutils.escape(self._replace(value))))
        self._out.write('>')

    def endElement(self, name):
        self._out.write('</%s>' % self._internName(name))

    def characters(self, content):
        self._out.write(saxutils.escape(self._replace(content)))

    def ignorableWhitespace(self, content):
        self._out.write(content)
        
    def processingInstruction(self, target, data):
        self._out.write('<?%s %s?>' % (self._internName(target), self._replace(data)))

parser = make_parser()
parser.setContentHandler(ContentGenerator())
parser.parse(sys.argv[1])

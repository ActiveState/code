# echoxml.py

import sys
from xml.sax import sax2exts, saxutils, handler
from xml.sax import SAXNotSupportedException, SAXNotRecognizedException

class EchoGenerator(saxutils.XMLGenerator):

    def __init__(self, out=None, encoding="iso-8859-1"):
        saxutils.XMLGenerator.__init__(self, out, encoding)
        self._in_entity = 0
        self._in_cdata = 0

    def characters(self, content):
        if self._in_entity:
            return
        elif self._in_cdata:
            self._out.write(content)
        else:
            saxutils.XMLGenerator.characters(self, content)

    # -- LexicalHandler interface

    def comment(self, content):
        self._out.write('<!--%s-->' % content)

    def startDTD(self, name, public_id, system_id):
        self._out.write('<!DOCTYPE %s' % name)
        if public_id:
            self._out.write(' PUBLIC %s %s' % (
                saxutils.quoteattr(public_id),
                saxutils.quoteattr(system_id)))
        elif system_id:
            self._out.write(' SYSTEM %s' % saxutils.quoteattr(system_id))

    def endDTD(self):
        self._out.write('>\n')

    def startEntity(self, name):
        self._out.write('&%s;' % name)
        self._in_entity = 1

    def endEntity(self, name):
        self._in_entity = 0

    def startCDATA(self):
        self._out.write('<![CDATA[')
        self._in_cdata = 1

    def endCDATA(self):
        self._out.write(']]>')
        self._in_cdata = 0


def test(xmlfile):
    parser = sax2exts.make_parser([
        'pirxx',
        'xml.sax.drivers2.drv_xmlproc',
        'xml.sax.drivers2.drv_pyexpat',
    ])
    print >>sys.stderr, "*** Using", parser

    try:
        parser.setFeature(handler.feature_namespaces, 1)
    except (SAXNotRecognizedException, SAXNotSupportedException):
        pass
    try:
        parser.setFeature(handler.feature_validation, 0)
    except (SAXNotRecognizedException, SAXNotSupportedException):
        pass

    saxhandler = EchoGenerator()
    parser.setContentHandler(saxhandler)
    parser.setProperty(handler.property_lexical_handler, saxhandler)
    parser.parse(xmlfile)


if __name__ == "__main__":
    test('books.xml')

#!/usr/bin/python2.1 
import sys 
from xml.dom.ext import SplitQName 
from xml.sax.handler import ContentHandler 
from xml.sax.saxutils import escape

_ROOT, _STRING, _COMMENT, _NAME, _KEYWORD, _TEXT, _HEAD =0,1,2,3,4,5,6 
DOCBOOK = {
    _ROOT: ('<programlisting>','</programlisting>'),
    _STRING: ('<emphasis>', '</emphasis>'),
    _COMMENT:('<emphasis>', '</emphasis>'),
    _NAME:  ('', ''),
    _KEYWORD:('<emphasis role="bold">', '</emphasis>'),
    _TEXT:  ('', '')
    } HTML = {
    _ROOT: ('<div>', '</div>'),
    _STRING: ('<font color="#004080">', '</font>'),
    _COMMENT:('<font color="#008000">', '</font>'),
    _NAME:  ('', ''),
    _KEYWORD:('<font color="#C00000">', '</font>'),
    _TEXT:  ('', '')
    } 

class XmlFormatSaxHandler(ContentHandler):
    ''' format an xmlfile to docbook or html '''
    
    def __init__(self, head=1, output=sys.stdout, encoding='UTF-8'):
        self._out = output
        self._cod = encoding
        self._o_d = DOCBOOK
        self._in_cdata = 0
        self._in_entity = 0

    def set_format(self, format):
        if format == 'docbook':
            self._o_d = DOCBOOK
        if format == 'html':
            self._o_d = HTML
            
    ## content handler #####################################################
    def startDocument(self):
        self._out.write(self._o_d[_ROOT][0])
            
    def endDocument(self):
        self._out.write(self._o_d[_ROOT][1])
        
    def startElement(self, name, attrs):
        prefix, local = SplitQName(name)
        if prefix:
            self._out.write('&lt;%s%s%s:%s%s%s'.encode(self._cod) % (
                self._o_d[_KEYWORD][0], prefix, self._o_d[_KEYWORD][1],
                self._o_d[_NAME][0], local, self._o_d[_NAME][1]))
        else:
            self._out.write('&lt;%s%s%s'.encode(self._cod) % (
                self._o_d[_NAME][0], local, self._o_d[_NAME][1]))
        for key, val in attrs.items():
            prefix, local = SplitQName(key)
            if prefix:
                self._out.write('%s%s%s:%s%s%s=%s"%s"%s'.encode(self._cod) % (
                    self._o_d[_KEYWORD][0], prefix, self._o_d[_KEYWORD][1],
                    self._o_d[_NAME][0], local, self._o_d[_NAME][1],
                    self._o_d[_STRING][0], val, self._o_d[_STRING][1]))
            else:
                self._out.write(' %s%s%s=%s"%s"%s'.encode(self._cod) % (
                    self._o_d[_NAME][0], local, self._o_d[_NAME][1],
                    self._o_d[_STRING][0], val, self._o_d[_STRING][1]))
        self._out.write('>')
        
    def endElement(self, name):
        prefix, local = SplitQName(name)
        if prefix:
            self._out.write('&lt;/%s%s%s:%s%s%s>'.encode(self._cod) % (
                self._o_d[_KEYWORD][0], prefix, self._o_d[_KEYWORD][1],
                self._o_d[_NAME][0], local, self._o_d[_NAME][1]))
        else:
            self._out.write('&lt;/%s%s%s>'.encode(self._cod) % (
                self._o_d[_NAME][0], local, self._o_d[_NAME][1]))
        
    def processingInstruction(self, target, data):
        self._out.write('&lt;?%s%s%s %s%s%s>'.encode(self._cod) % (
            self._o_d[_NAME][0], target, self._o_d[_NAME][1],
            self._o_d[_STRING][0], data, self._o_d[_STRING][1]))
        
    def characters(self, ch):
        if self._in_entity: return
	elif not self._in_cdata: ch = escape(ch)
        self._out.write('%s%s%s' % (
            self._o_d[_TEXT][0], ch.encode(self._cod), self._o_d[_TEXT][1]))
        
    ## lexical handler #####################################################
    def comment(self, comment):
        self._out.write('%s&lt;!--%s-->%s' % (
            self._o_d[_COMMENT][0],
            comment.replace('<', '&lt;').encode(self._cod),
            self._o_d[_COMMENT][1]))
        
    def startCDATA(self):
        self._out.write('&lt;%s[CDATA[%s' % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1]))
        self._in_cdata = 1
        
    def endCDATA(self):
        self._out.write('%s]]%s>' % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1]))
        self._in_cdata = 0
        
    def startDTD(self, name, public_id, system_id):
        self._out.write('&lt;%s!DOCTYPE%s %s'.encode(self._cod) % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], name))
        if public_id:
            self._out.write(' PUBLIC %s"%s"%s %s"%s"%s['.encode(self._cod) % (
                self._o_d[_STRING][0], public_id, self._o_d[_STRING][1],
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))
        else:
            self._out.write(' SYSTEM %s"%s"%s ['.encode(self._cod) % (
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))
            
    def endDTD(self):
        self._out.write(']>')

    def startEntity(self, name):
        self._out.write('%s&%s;%s'.encode(self._cod) % (
                        self._o_d[_NAME][0], name, self._o_d[_NAME][1]))
        self._in_entity = 1

    def endEntity(self, name):
        self._in_entity = 0
        
    ## decl handler ########################################################
    def internalEntityDecl(self, name, value):
        self._out.write('&lt;%s!ENTITY%s %s'.encode(self._cod) % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], name))
        if public_id:
            self._out.write(' PUBLIC %s"%s"%s %s
                self._o_d[_STRING][0], public_id, self._o_d[_STRING][1],
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))
        else:
            self._out.write(' SYSTEM %s"%s"%s>'.encode(self._cod) % (
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))
            
    def externalEntityDecl(self, name, public_id, system_id):
        self._out.write('&lt;%s!ENTITY%s %s'.encode(self._cod) % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], name))
        if public_id:
            self._out.write(' PUBLIC %s"%s"%s %s"%s"%s>'.encode(self._cod)%(
                self._o_d[_STRING][0], public_id, self._o_d[_STRING][1],
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))
        else:
            self._out.write(' SYSTEM %s"%s"%s>'.encode(self._cod) % (
                self._o_d[_STRING][0], system_id, self._o_d[_STRING][1]))

    def elementDecl(self, elem_name, content_model):
        c_m = _decode_content_model(content_model)
        self._out.write('&lt;%s!ELEMENT%s %s %s>'.encode(self._cod) % (
            self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], elem_name,
            c_m))
        
    def attributeDecl(self,elem_name,attr_name,type_d,value_def,value):
        import types
        if type(type_d) is types.ListType:
            s = ''
            for pos in type_d:
                if not s:
                    s = '(%s' % pos
                else:
                    s = '%s|%s' % (s, pos)
            s = '%s)' % s
            self._out.write('&lt;%s!ATTLIST%s %s %s %s%s>'.encode(self._cod)%(
                self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], elem_name,
                attr_name, s , value_def))
        else:
            self._out.write('&lt;%s!ATTLIST%s %s %s%s>'.encode(self._cod)%(
                self._o_d[_KEYWORD][0], self._o_d[_KEYWORD][1], elem_name,
                attr_name, type))
            
C_OP, C_VAL, C_NUM = 0, 1, 2 
def _decode_content_model(content_m):
    ''' recursively decode a content_model returned by parsers in 
	elementDecl '''
    s = ''
    if content_m[C_OP] == ',':
        for c_m in content_m[C_VAL]:
            if not s:
                s = '(%s' % _decode_content_model(c_m)
            else:
                s = '%s, %s' % (s, _decode_content_model(c_m))
        s = '%s)%s' % (s, content_m[C_NUM] )
    elif content_m[C_OP] == '|':
        for c_m in content_m[C_VAL]:
            if not s:
                s = '(%s' % _decode_content_model(c_m)
            else:
                s = '%s|%s' % (s, _decode_content_model(c_m))
        s = '%s)%s' % (s, content_m[C_NUM] )
    else:
        s = '%s%s' % (s, content_m[C_OP])
        s = '%s%s' % (s, content_m[-1])
    return s
            
USAGE = '''xml2dcbk: format xml source code to xml docbook using roles
Usage: xml2dcbk [options] source.py..., parse XML file(s)
       xml2dcbk -h/--help, print this help message and exit Options:
       _ -e/--encoding iso-8859-1, specify encoding to use in outputs
       _ -d/--docbook, format output as docbook xml (default)
       _ -w/--html, format output in html instead of docbook ''' 

def run(args):
    import getopt, os
    from xml.sax import make_parser
    from xml.sax.handler import property_lexical_handler,\
         property_declaration_handler
    ## get options
    (opt, args) = getopt.getopt(args, 'he:dw',
                                ['help', 'encoding=', 'docbook', 'html'])
    encod, format = 'UTF-8', 'docbook'
    for o in opt:
        if o[0] == '-h' or o[0] == '--help':
            print USAGE
            return
        elif o[0] == '-d' or o[0] == '--docbook':
            format = 'docbook'
        elif o[0] == '-w' or o[0] == '--html':
            format = 'html'
        elif o[0] == '-e' or o[0] == '--encoding':
            encod = o[1]
                
    ## transforms source files (xmlproc support property_lexical_handler while
    ## pyexpat doen't)
    p = make_parser(['xml.sax.drivers2.drv_xmlproc'])
    for file in args:
        source = open(file, 'r')
        ## prepare handler
        if file[-4:] != '.xml':
            print >>sys.stderr, 'Unknown extension %s, ignored file %s'%(
                file[-4:], file)
            continue
        dest = open('%s_dcbk.xml' % os.path.basename(file)[:-4], 'w+')
        h = XmlFormatSaxHandler(dest, encod)
        h.set_format(format)
        p.setContentHandler(h)
        try:
            p.setProperty(property_lexical_handler, h)
        except Exception, e:
            print e
        try:
            p.setProperty(property_declaration_handler, h)
        except Exception, e:
            print e
        print >>sys.stderr, "Formatting %s ..." % file
        ## parse and write colorized version to output file
        p.parse(source)
        
        source.close()
        dest.close()
    
if __name__ == "__main__":
    run(sys.argv[1:])

import StringIO, sys
from xml import sax
from xml.sax import handler, saxutils, xmlreader

RDF_NS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

class RDFFilter (saxutils.XMLFilterBase):
    def __init__ (self, *args):
        saxutils.XMLFilterBase.__init__(self, *args)
        self.in_rdf_stack = [False]

    def startElementNS (self, (uri, localname), qname, attrs):
        if uri == RDF_NS or self.in_rdf_stack[0] == True:
            self.in_rdf_stack.insert(0, True)
            return

        # Delete attributes that belong to the RDF namespace
        dict = {}
        for key, value in attrs.items():
            uri, localname = key
            if uri != RDF_NS:
                dict[key] = value
                
        attrs = xmlreader.AttributesNSImpl(dict, attrs.getQNames())
            
        self.in_rdf_stack.insert(0, self.in_rdf_stack[0])
        
        saxutils.XMLFilterBase.startElementNS(self,
                                              (uri, localname), qname, attrs)
    
    def characters(self, content):
        if self.in_rdf_stack[0]:
            return
        saxutils.XMLFilterBase.characters(self, content)
        
    def endElementNS (self, (uri, localname), qname):
        if self.in_rdf_stack.pop(0) == True:
            return
        saxutils.XMLFilterBase.endElementNS(self,
                                            (uri, localname), qname)

def filter_rdf (input, output):
    """filter_rdf(input:file, output:file)

    Parses the XML input from the input stream, filtering out all
    elements and attributes that are in the RDF namespace.
    """

    output_gen = saxutils.XMLGenerator(output)
    parser = sax.make_parser()
    filter = RDFFilter(parser)
    filter.setFeature(handler.feature_namespaces, True)
    filter.setContentHandler(output_gen)
    filter.setErrorHandler(handler.ErrorHandler())
    filter.parse(input)

if __name__ == '__main__':
    TEST_RDF = '''<?xml version="1.0"?>
<metadata xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
   <title>  This is non-RDF content </title>
   <rdf:RDF>
     <rdf:Description rdf:about="%s">
       <dc:Creator>%s</dc:Creator>
     </rdf:Description>
   </rdf:RDF>
  <element />
</metadata>
''' 
    input = StringIO.StringIO(TEST_RDF)
    filter_rdf(input, sys.stdout)

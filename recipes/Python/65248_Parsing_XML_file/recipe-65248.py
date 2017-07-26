import xml.parsers.expat, sys

class MyXML:
        Parser = ""

        # prepare for parsing

        def __init__(self, xml_file):
                assert(xml_file != "")
                self.Parser = xml.parsers.expat.ParserCreate()

                self.Parser.CharacterDataHandler = self.handleCharData
                self.Parser.StartElementHandler = self.handleStartElement
                self.Parser.EndElementHandler = self.handleEndElement

        # parse the XML file
  
        def parse(self):
                try:
                        self.Parser.ParseFile(open(xml_file, "r"))
                except:
                        print "ERROR: Can't open XML file!"
                        sys.exit(0)

         # will be overwritten w/ implementation specific methods

        def handleCharData(self, data): pass
        def handleStartElement(self, name, attrs): pass
        def handleEndElement(self, name): pass

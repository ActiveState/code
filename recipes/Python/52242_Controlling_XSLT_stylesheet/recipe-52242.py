from xml.xslt.Processor import Processor
from xml.xslt.StylesheetReader import StylesheetReader

class StylesheetFromDict(StylesheetReader):
    "A stylesheet reader that loads XSLT stylesheets from a python dictionary"

    def __init__(self, styles, *args):
        "Remember the dict we want to load the stylesheets from"
        apply(StylesheetReader.__init__, (self,) + args)
        self.styles = styles
        self.__myargs = args

    def __getinitargs__(self):
        "Return init args for clone()"
        return (self.styles,) + self.__myargs

    def fromUri(self, uri, baseUri='', ownerDoc=None, stripElements=None):
        "Load stylesheet from a dict"
        parts = uri.split(':', 1)
        if parts[0] == 'internal' and self.styles.has_key(parts[1]):
            # load the stylesheet from the internal repository (our dict)
            return StylesheetReader.fromString(self, self.styles[parts[1]],
                baseUri, ownerDoc, stripElements)
        else:
            # revert to normal behaviour
            return StylesheetReader.fromUri(self, uri,
                baseUri, ownerDoc, stripElements)

if __name__ == "__main__":
    # the sample stylesheet repository
    internal_stylesheets = {
        'second-author.xsl': """
            <person xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xsl:version="1.0">
            <xsl:value-of select="books/book/author[2]"/>
            </person>
        """
    }

    # the sample document, referring to an "internal" stylesheet
    xmldoc = """
      <?xml-stylesheet href="internal:second-author.xsl" type="text/xml"?>
      <books>
        <book title="Python Essential Reference">
          <author>David M. Beazley</author>
          <author>Guido van Rossum</author>
        </book>
      </books>
    """

    # create XSLT processor and run it
    processor = Processor()
    processor.setStylesheetReader(StylesheetFromDict(internal_stylesheets))
    print processor.runString(xmldoc)

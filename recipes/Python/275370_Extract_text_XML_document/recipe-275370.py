from sgmllib import SGMLParser

class XMLJustText ( SGMLParser ) :
    def handle_data ( self, data ) :
        print data

XMLJustText  ( ) . feed ( 
"<items><item>text 1</item><item>text 2</item></items>" 
)

import string

class Stripper( SGMLParser ) :
    ...
    
    def handle_data( self, data ) :
        data = string.replace( data, '\r', '' )
        ...

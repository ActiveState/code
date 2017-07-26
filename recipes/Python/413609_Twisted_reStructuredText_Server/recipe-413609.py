PORT = 8080                                                                     
PATH = '/tmp/'                                                                  
EXTENSION = '.rst'                                                              
                                                                                
from twisted.web.resource import Resource                                       
from twisted.web import server                                                  
from twisted.web import static                                                  
from twisted.internet import reactor
                                            
from docutils.core import publish_string                                                                  
                                                      
class ReStructured( Resource ):                                                                                                                                 
    def __init__( self, filename, *a ):                                         
        self.rst = open( filename ).read( )                                                                                                               
                                                                                
    def render( self, request ):                                                
        return publish_string( self.rst, writer_name = 'html' )                 
                                                                                

resource = static.File( PATH )                                                  
resource.processors = { EXTENSION : ReStructured }                              
resource.indexNames = [ 'index' + EXTENSION ]                                   
                                                                                
reactor.listenTCP(                                                              
        PORT,                                                                   
        server.Site( resource )                                                 
        )                                                                       
reactor.run( )            

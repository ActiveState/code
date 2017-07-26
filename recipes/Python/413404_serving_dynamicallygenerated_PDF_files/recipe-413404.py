#################################################################
#################################################################
import xmlrpclib
from cherrypy.lib.filter.xmlrpcfilter import XmlRpcFilter
from cherrypy import cpg
from reportlab.pdfgen import canvas


class Root:
  _cpFilterList = [XmlRpcFilter()]

  def _cpOnError(self):
    import traceback, StringIO
    bodyFile = StringIO.StringIO()
    traceback.print_exc(file = bodyFile)
    errorBody = bodyFile.getvalue()
    if cpg.request.isRPC: 
      ## isRPC boolean is set on xml-rpc requests by the filter
      ## convert the traceback to a dumped Fault object: 
      ## the XML-RPC exception
      cpg.response.body = [xmlrpclib.dumps(xmlrpclib.Fault(1,errorBody))]
    else:
      ## handle regular web errors
      cpg.response.body = ['<pre>%s</pre>' % errorBody]
      
  def getPdf(self,aMsg):
    c = canvas.Canvas(None)
    c.drawString(100,100,aMsg)
    c.showPage()
    c.save()
    return xmlrpclib.Binary(c.getpdfdata())
   
  getPdf.exposed = True 

cpg.root = Root()
if __name__=='__main__':
  cpg.server.start(configMap = {'socketPort': 9001,
                                'threadPool':0,
                                'socketQueueSize':10 })
########################################################
########################################################

# a simple client ######################################
########################################################
import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:9001')
f = open('helloWorld.pdf','w')
f.write(server.getPdf('Hello World!').data)
f.close()
########################################################
########################################################

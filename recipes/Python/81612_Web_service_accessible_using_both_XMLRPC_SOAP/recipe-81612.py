# The actual web service.

import netsvc
import netsvc.xmlrpc
import netsvc.soap
import signal
import dbm
 
class Database(netsvc.Service):
 
  def __init__(self,name):
    netsvc.Service.__init__(self,name)
    self._db = dbm.open(name,'c')
    self.exportMethod(self.get)
    self.exportMethod(self.put)
    self.exportMethod(self.keys)
    self.joinGroup("web-services")
 
  def get(self,key):
    return self._db[key]
 
  def put(self,key,value):
    self._db[key] = value
 
  def keys(self):
    return self._db.keys()
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
httpd = netsvc.HttpDaemon(8000)
 
database = Database("test")
 
rpcgw1 = netsvc.xmlrpc.RpcGateway("web-services")
httpd.attach("/xmlrpc/database",rpcgw1)
 
rpcgw2 = netsvc.soap.RpcGateway("web-services")
httpd.attach("/soap/database",rpcgw2)
 
httpd.start()
dispatcher.run()

# An XML-RPC client using PythonWare "xmlrpclib" module.

import xmlrpclib
 
url = "http://localhost:8000/xmlrpc/database/test"
service = xmlrpclib.Server(url)
 
for i in range(10):
  service.put(str(i),str(i*i))
 
for key in service.keys():
  print key,service.get(key)

# A SOAP client using pywebsvcs "SOAP" module.

import SOAP
 
url = "http://localhost:8000/soap/database/test"
service = SOAP.SOAPProxy(url)
 
for i in range(10):
  service.put(str(i),str(i*i))
 
for key in service.keys():
  print key,service.get(key)

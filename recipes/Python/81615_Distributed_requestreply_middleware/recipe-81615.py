# The exchange process which everything connects to.

import netsvc
import signal
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_SERVER)
exchange.listen(11111)
 
dispatcher.run()

# The server side of the interaction.

import netsvc
import signal
 
class Service(netsvc.Service):
 
  def __init__(self):
    netsvc.Service.__init__(self,"math")
    self.joinGroup("web-services")
    self.exportMethod(self.multiply)
 
  def multiply(self,x,y):
    return x*y
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
exchange.connect("localhost",11111,5)
 
service = Service()
 
dispatcher.run()

# The client side of the interaction.

import netsvc
import signal
import random
 
class Client(netsvc.Service):
 
  def __init__(self):
    netsvc.Service.__init__(self,"")
    self.startTimer(self.call,1,"1")
 
  def call(self,name):
    service = self.serviceEndPoint("math")
    if service != None:
      x = int(random.random()*1000)
      id = service.multiply(x,x)
      self.monitorResponse(self.result,id)
    self.startTimer(self.call,1,"1")
 
  def result(self,square):
    print square
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
exchange.connect("localhost",11111,5)
 
client = Client()
 
dispatcher.run()

# A gateway which allows XML-RPC style requests to the same service.

import signal
import netsvc
import netsvc.xmlrpc
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
httpd = netsvc.HttpDaemon(8000)
rpcgw = netsvc.xmlrpc.RpcGateway("web-services")
httpd.attach("/xmlrpc/service",rpcgw)
httpd.start()
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
exchange.connect("localhost",11111,5)
 
dispatcher.run()

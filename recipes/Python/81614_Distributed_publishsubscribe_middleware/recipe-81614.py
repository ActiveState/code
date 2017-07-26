# The exchange process which everything connects to.

import netsvc
import signal
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_SERVER)
exchange.listen(11111)
 
dispatcher.run()

# Service which periodically publishes information.

import netsvc
import signal
import random
 
class Publisher(netsvc.Service):
 
  def __init__(self):
    netsvc.Service.__init__(self,"SEED")
    self._count = 0
    time = netsvc.DateTime()
    data = { "time": time }
    self.publishReport("init",data,-1)
    self.startTimer(self.publish,1,"1")
 
  def publish(self,name):
    self._count = self._count + 1
    time = netsvc.DateTime()
    value = int(0xFFFF*random.random())
    data = { "time": time, "count": self._count, "value": value }
    self.publishReport("next",data)
    self.startTimer(self.publish,1,"1")
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
exchange.connect("localhost",11111,5)
 
publisher = Publisher()
 
dispatcher.run()

# Service which subscribes to published information.

import netsvc
import signal
 
class Subscriber(netsvc.Service):
 
  def __init__(self):
    netsvc.Service.__init__(self)
    self.monitorReports(self.seed,"SEED","next")
 
  def seed(self,service,subjectName,content):
    print "%s - %s" % (content["time"],content["value"])
 
dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)
 
exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
exchange.connect("localhost",11111,5)
 
subscriber = Subscriber()
 
dispatcher.run()

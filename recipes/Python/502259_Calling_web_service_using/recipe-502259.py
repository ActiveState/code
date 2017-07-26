#import the WSDL module, this does all the work for you.
from SOAPpy import WSDL

#specify the wsdl file. This file contains everything an application needs to know
#to call the service with the right arguments, with the right protocol at the right
#location etc.
WSDLFile   = "http://developerdays.com/cgi-bin/tempconverter.exe/wsdl/ITempConverter"

#Create a proxy. You can call methods that are on a distant machine as if they were
#on your local machine, as if they were implemented in the proxy object.

proxy      = WSDL.Proxy(WSDLFile)
#uncomment thoses lines to see outgoing and incoming soap envelops
#proxy.soapserver.config.dumpSOAPIn=1
#proxy.soapserver.config.dumpSOAPOut=1

Centigrades = 12

#Here we call the action CtoF as if were a method defined in the proxy object.
Faranheites  = proxy.CtoF(Centigrades)

print "%s Centigrades = %s Faranheites" % (Centigrades,Faranheites)

## trace :
## chaouche@CAY:~/TEST$ python soapCentigradesToFaranheites.py
## 12 Centigrades = 32 Faranheites
## chaouche@CAY:~/TEST$

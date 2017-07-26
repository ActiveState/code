import base64
from array import array


class StupidSimpleDataMarshal:
    def SendData(self, var):
        return base64.b64encode(var.__repr__())
    
    def ReceiveData(self, Data):
        return eval(base64.b64decode(Data))
    
################################################################################



x = dict()

x["myString"]       = "TestString"
x["myFloat"]        = 5.764
x["myList"]         = ["Blah", "Crap"]
x["myDict"]         = {'Bob':"Is Cool", 'Terry':"Is A Jerk"}
x["myBinaryArray"]  = array('B', "Uber Amounts of Binary Data")

SSDM = StupidSimpleDataMarshal()

dataToSocket    = SSDM.SendData(x)
dataFromSocket  = SSDM.ReceiveData(dataToSocket)

print dataToSocket

for k, v in dataFromSocket.iteritems():
    print k, v, type(v)

  

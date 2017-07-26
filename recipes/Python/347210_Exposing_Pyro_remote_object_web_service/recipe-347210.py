#########################################################
# The object (file object.py)

class myObject:
    def __init__(self):
        # a global counter
        self.globalNumCalls = 0
    def method1(self, string):
        self.globalNumCalls += 1
        return len(string)
    def method2(self, number):
        self.globalNumCalls += 1
        return number*number
    def getGlobalNumCalls(self):
        return self.globalNumCalls

def remote_objects():
	return { 'sampleObject': myObject() }
#########################################################
#########################################################


#########################################################
# The Pyro server, with a wrapper for object.myobject 
# and thread local storage (file server.py)

import sys
import Pyro.core
import Pyro.naming

import object


class SampleObject(Pyro.core.ObjBase, object.myObject):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        object.myObject.__init__(self)
        
    def method2localcount(self, number):
        # increment the thread-local counter
        self.getLocalStorage().numSquareCalls += 1
        # call the "standard" function (this will increment the global counter)
        return self.method2(number)
    
    def getNumLocalSquareCalls(self):
        return self.getLocalStorage().numSquareCalls

def initTLS(tls):
        print "Init TLS:",tls
        print "Setting a counter, numSquareCalls, for this TLS to 0."
        tls.numSquareCalls=0
                

if __name__ == "__main__":
    Pyro.core.initServer()
    daemon=Pyro.core.Daemon()
    daemon.useNameServer(Pyro.naming.NameServerLocator().getNS())
    daemon.setInitTLS(initTLS)
    uri=daemon.connect(SampleObject(), "sampleObject")
    print "sample object is running."
    daemon.setTimeout(5)
    daemon.requestLoop()
#########################################################
#########################################################


#########################################################
# The cherrypy server definition file (file testXmlRpc.cpy)

def initProgram():
    import Pyro.core

def initThread(threadIndex):
    time.sleep(threadIndex * 0.2)
    # dispatch a pyro object to each thread via "request" reserved variable
    Pyro.core.initClient()
    request.x=Pyro.core.getProxyForURI("PYRONAME://sampleObject")
    request.x._setTimeout(5)
    request.x._release()
    
CherryClass Xml_rpc:

view:
    def lenString(self, a) xmlrpc:
        # Return the length of its input string
        return request.x.method1(a)
    def squareNumber(self, a) xmlrpc:
        # Return the square of its input number
        return request.x.method2(a)
    def squareNumberLocalCount(self, a) xmlrpc:
        # Return the square of its input number, incrementing a thread local counter, too.
        return request.x.method2localcount(a)
    def noglobalcalls(self) xmlrpc:
        # Return the number of global calls
        return request.x.getGlobalNumCalls()
    def nosquarelocalcalls(self) xmlrpc:
        # Return the number of thread-local calls
        return request.x.getNumLocalSquareCalls()
#########################################################
#########################################################


#########################################################
# The cherrypy configuration file (file testXmlRpcServer.cfg)
[server]
typeOfRequests=xmlRpc,web
threadPool=3
#########################################################
#########################################################


#########################################################
# A sample test program (file testXmlRpcClient.py)

import xmlrpclib, time
testsvr = xmlrpclib.Server("http://localhost:8000")

sttime = time.time()
    
for i in xrange(1000):
    assert len("I love cherry pie") == testsvr.xml.rpc.lenString("I love cherry pie")
    assert testsvr.xml.rpc.squareNumber(12) == 144
    print "# global calls:", testsvr.xml.rpc.noglobalcalls()
    assert testsvr.xml.rpc.squareNumberLocalCount(6) == 36
    print "# thread-local calls: ", testsvr.xml.rpc.nosquarelocalcalls()
print time.time() - sttime
#########################################################
#########################################################

# a python COM object (it's a standard sample, I've reported it here only 
# to let the recipe be complete (file testcomserver.py).

##################################################
class HelloWorld:
    _reg_clsid_ = "{7CC9F362-486D-11D1-BB48-0000E838A65F}"
    _reg_desc_ = "Python Test COM Server"
    _reg_progid_ = "Python.TestServer"
    # Next line assumes file is "testcomserver.py"
    _reg_class_spec_ = "testcomserver.HelloWorld"
    _public_methods_ = ['Hello']
    _public_attrs_ = ['softspace', 'noCalls']
    _readonly_attrs_ = ['noCalls']
    
    def __init__(self):
        self.softspace = 1
        self.noCalls = 0
    def Hello(self, who):
        self.noCalls = self.noCalls + 1
        # insert "softspace" number of spaces
        return "Hello" + " " * self.softspace + str(who)

if __name__=='__main__':
    import win32com.server.register
    win32com.server.register.UseCommandLine(HelloWorld)
##################################################
##################################################

##################################################
# the CherryPy (v.0.10) server definition file (file testXmlRpc.cpy)
def initProgram():
    import win32com.client, pythoncom, time

def initThread(threadIndex):
    time.sleep(threadIndex * 0.2)
    # start the COM environment in a MT situation
    pythoncom.CoInitialize()
    # dispatch a COM object to each thread via "request" reserved variable
    request.x=win32com.client.Dispatch("Python.TestServer")


CherryClass Xml_rpc:

view:
    def hello(self, a) xmlrpc:
        # Return the COM hello method
        return request.x.hello(a)
    def nocalls(self) xmlrpc:
        # Return the COM noCalls variable
        return request.x.noCalls
##################################################
##################################################

##################################################
# the CherryPy server configuration file (file testXmlRpcServer.cfg)
[server]
typeOfRequests=xmlRpc,web
threadPool=3
##################################################
##################################################

##################################################
# a client test program 
import xmlrpclib, time
if __name__=='__main__':
    testsvr = xmlrpclib.Server("http://127.0.0.1:8000")
    print testsvr.xml.rpc.hello("I love cherry pie " + str(x))
    print testsvr.xml.rpc.nocalls()
    raw_input("press a key:...")
##################################################
##################################################

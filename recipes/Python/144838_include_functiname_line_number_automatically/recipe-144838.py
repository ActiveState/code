#messaging.py
#this is a module used for messaging.  It allows multiple classes
#to handle various types of messages.  It should work on all python
#versions >= 1.5.2

import sys, string, exceptions

#this flag determines whether debug output is sent to debug handlers themselves
debug = 1

def setDebugging(debugging):
    global debug
    debug = debugging

class MessagingException(exceptions.Exception):
    """an exception class for any errors that may occur in 
    a messaging function"""
    def __init__(self, args=None):
        self.args = args

class FakeException(exceptions.Exception):
    """an exception that is thrown and then caught
    to get a reference to the current execution frame"""
    pass        
        
        
class MessageHandler:
    """All message handlers should inherit this class.  Each method will be 
    passed a string when the executing program passes calls a messaging function"""
    def handleStdMsg(self, msg):
        """do something with a standard message from the program"""
        pass
    def handleErrMsg(self, msg):
        """do something with an error message.  This will already include the
        class, method, and line of the call"""
        pass
    def handleDbgMsg(self, msg):
        """do something with a debug message.  This will already include the
        class, method, and line of the call"""
        pass

class defaultMessageHandler(MessageHandler):
    """This is a default message handler.  It simply spits all strings to
    standard out"""
    def handleStdMsg(self, msg):
        sys.stdout.write(msg + "\n")
    def handleErrMsg(self, msg):
        sys.stderr.write(msg + "\n")
    def handleDbgMsg(self, msg):
        sys.stdout.write(msg + "\n")

#this keeps track of the handlers
_messageHandlers = []

#call this with the handler to register it for receiving messages
def registerMessageHandler(handler):
    """we're not going to check for inheritance, but we should check to make
    sure that it has the correct methods"""
    for methodName in ["handleStdMsg", "handleErrMsg", "handleDbgMsg"]:
        try:
            getattr(handler, methodName)
        except:            
            raise MessagingException, "The class " + handler.__class__.__name__ + " is missing a " + methodName + " method"
    _messageHandlers.append(handler)
    
    
def getCallString(level):
    #this gets us the frame of the caller and will work
    #in python versions 1.5.2 and greater (there are better
    #ways starting in 2.1
    try:
        raise FakeException("this is fake")
    except Exception, e:
        #get the current execution frame
        f = sys.exc_info()[2].tb_frame
    #go back as many call-frames as was specified
    while level >= 0:        
        f = f.f_back
        level = level-1
    #if there is a self variable in the caller's local namespace then
    #we'll make the assumption that the caller is a class method
    obj = f.f_locals.get("self", None)
    functionName = f.f_code.co_name
    if obj:
        callStr = obj.__class__.__name__+"::"+f.f_code.co_name+" (line "+str(f.f_lineno)+")"
    else:
        callStr = f.f_code.co_name+" (line "+str(f.f_lineno)+")"        
    return callStr        
    
#send this message to all handlers of std messages
def stdMsg(*args):
    stdStr = string.join(map(str, args), " ")
    for handler in _messageHandlers:
        handler.handleStdMsg(stdStr)

#send this message to all handlers of error messages
def errMsg(*args):
    errStr = "Error in "+getCallString(1)+" : "+string.join(map(str, args), " ")
    for handler in _messageHandlers:
        handler.handleErrMsg(errStr)

#send this message to all handlers of debug messages
def dbgMsg(*args):
    if not debug:
        return
    errStr = getCallString(1)+" : "+string.join(map(str, args), " ")
    for handler in _messageHandlers:
        handler.handleDbgMsg(errStr)


registerMessageHandler(defaultMessageHandler())
#end of messaging.py

#test.py
#here is a simple use case for the above module
from messaging import stdMsg, dbgMsg, errMsg, setDebugging

setDebugging(0)

dbgMsg("this won't be printed")
stdMsg("but this will")

setDebugging(1)

def foo():
    dbgMsg("this is a debug message in", "foo")
    
class bar:
    def baz(self):
        errMsg("this is an error message in bar")

foo()
b = bar()
b.baz()
#end of test.py

output is :
but this will
foo (line 12) : this is a debug message in foo
Error in bar::baz (line 16) : this is an error message in bar
 

import sys, traceback, string, os
from datetime import datetime

"""
XceptionHandler: Rev 4

Change Log:

04/2/2010    -Added option to allow for exception to be raised rather than
             returned and still have logging and messaging options as well

04/2/2010    -Added option for overriding default logging by passing in a logging 
             object of the main project or parent class

04/6/2010    -Replace query builder with raw traceback dump return to allow more
              code flexibility
              
INIT VARS:

DEBUG       bool   Turn ON/OFF Debug Messages

LOG_FILE    str    Name of Logfile default to XceptLog.txt

LOG_TABLE   str    Name of LOGGING DB TABLE if used input query and data tuple
                   are generated for feeding into MySQLdb or SQLlite

MSG_TYPE    str    Detailed or Simple Versions of Debug Messages

EXC_RETURN  ref    Indicate an exception has occured and will be returned

EXC_RAISE   ref    Indicates an exception occured and to raise it rather than return

EXC_RAW     ref    Indicate and exception occured and will return traceback dump
                   as a dict.
                   
LOG_EVENTS  bool   Set default for logging can be overridden as needed in methods                   

"""

class XceptionHandler:

    def __init__(self, DEBUG=False, LOG_FILE="XceptLog.txt", LOG_TABLE="",
                 LOG_PATH= os.path.abspath(os.curdir)+os.sep+"xLOGS"+os.sep,  
                 MSG_TYPE="Detailed", EXC_RETURN=-1, EXC_RAW=-2, EXC_RAISE=-3, 
                 LOG_OBJ=None, LOG_EVENTS=False):
        
        self.xname      = str(self.__class__).split(".")[1]
        self.Debug      = DEBUG
        self.MSG_TYPE   = MSG_TYPE
        self.LOG_TABLE  = LOG_TABLE
        self.LOG_FILE   = LOG_FILE
        self.LOG_PATH   = LOG_PATH
        self.LOG_OBJ    = LOG_OBJ
        self.EXC_RETURN = EXC_RETURN
        self.EXC_RAISE  = EXC_RAISE
        self.EXC_RAW    = EXC_RAW
        self.LOG_EVENTS = LOG_EVENTS
        
        
    """
    Formatter for Debug Messages
    vars:
    ARGS    dict
    
    """    
    def ReturnFormat(self, ARGS, CallType):
        DetailedErr = ""
        
        DetailedErr1 = """
        --- EXCEPTION_ERROR ---
        File           : """+ARGS["filename"]
        
        DetailedErr2    = """
        Class          : """+ARGS["classname"]
        
        DetailedErr3    = """
        <CALL_TYPE>    : """+ARGS["methodname"]+"""
        Line           : """+ARGS["lineNumber"]+"""
        DTS            : """+str(datetime.now())+"""
        
        Exception Type : """+ARGS["exc_type"]+"""
        Exception Value: """+ARGS["exc_value"]+"""
        Exception Msg  : """+ARGS["exc_info"] +"""
        
        ------------------------
        """
        
        SimpleErr = """
        --- ERROR ---
        
        ErrorType : """+ARGS["exc_type"]+"""
        ErrorValue: """+ARGS["exc_value"]+"""
        ErrorMsg  : """+ARGS["exc_info"]+"""
        
        ------------------------
        """
        
        if self.MSG_TYPE == "Detailed":
            if CallType.find("Method") != -1:
                DetailedErr = DetailedErr1+DetailedErr2+DetailedErr3
            else:
                DetailedErr = DetailedErr1+DetailedErr3
                
            DetailedErr = DetailedErr.replace("<CALL_TYPE>", CallType)
            return DetailedErr
        else:
            return SimpleErr
        
        
        
    """
    Function exception handler
    Not intended to be directly called from the function but rather via ProcessReturn
    vars:
    retval    str
    
    """    
    def FunctionXHandler(self, retval):
        myObject            = sys.exc_info()[2]
        myTraceBack         = traceback.extract_tb(myObject)
        
        fileName            = myTraceBack[0][0]
        lineNumber          = str(myTraceBack[0][1])
        functionName        = myTraceBack[0][2]
        className           = " - "
        
        ARGS = dict()
        ARGS["filename"]    = fileName      
        ARGS["classname"]   = className
        ARGS["methodname"]  = functionName
        ARGS["lineNumber"]  = lineNumber
        ARGS["exc_type"]    = str(sys.exc_type)
        ARGS["exc_value"]   = str(sys.exc_value)
        ARGS["exc_info"]    = str(sys.exc_info()[0])
        ARGS["Message"]     = self.ReturnFormat(ARGS, "Function   ")
        
        return ARGS

    """
    Class Method exception handler
    Not intended to be directly called from the method but rather through ProcessReturn
    vars:
    className    str    Name of calling class
    """
    def ClassXHandler(self, className):
        myObject            = sys.exc_info()[2]
        myTraceBack         = traceback.extract_tb(myObject)
        
        fileName            = myTraceBack[0][0]
        lineNumber          = str(myTraceBack[0][1])
        methodName          = myTraceBack[0][2]
        
        ARGS = dict()
        ARGS["filename"]    = fileName   
        ARGS["Return"]      = ARGS.get("Return", "EXCEPTION_ERROR")
        ARGS["classname"]   = className
        ARGS["methodname"]  = methodName
        ARGS["lineNumber"]  = lineNumber
        ARGS["exc_type"]    = str(sys.exc_type)
        ARGS["exc_value"]   = str(sys.exc_value)
        ARGS["exc_info"]    = str(sys.exc_info()[0])
        ARGS["Message"]     = self.ReturnFormat(ARGS, "Method     ")
        
        if className == self.xname:
            print ARGS["Message"]
        return ARGS
  
  
  
  
    def ParseArgs(self, args):
        try:
            args    = args[0]
            retVal  = None
            logEvent= self.LOG_EVENTS
            logMsg  = ""
               
            if len(args)== 3:
                retVal=args[0] 
                if type(args[1]) == type(""):
                    logMsg = args[1]
                    logEvent = args[2]
                elif type(args[1]) == type(bool()):
                    logEvent = args[1]
                    logMsg   = args[2]
            elif len(args) == 2:
                retVal=args[0]                
                if type(args[1]) == type(""):
                    logMsg = args[1]
                else:
                    logEvent = args[1]
            elif len(args) == 1:
                retVal=args[0]
            
            return retVal, logEvent, logMsg
            
        except:
            return self.ClassXHandler(self.xname)
            
            
            
            
    """
     Main Method for handling return values, determine if exception/error/good
     and react accordingly
     vars:
     retVal       dynamicType    a -1 value indicates an exception
                                 and will return -1 gracefully.
                                 a -2 value indicates an exception
                                 and will return the raw traceback elements
                                 as a dict.
                                 a -3 value indicates an exception
                                 and will raise it.
                                 everything else is passed through
     className    str            name of calling class if called from a class
     logEvent     bool           True = logging, False = no logging
                                 2 = create DB query and data tuple
     logMsg       str            Custom pass though message to be logged
     
    """
    def ProcessReturn(self, className=None, *args):
        retVal, logEvent, logMsg = self.ParseArgs(args)
     
        ARGS = dict()
        
        if retVal == self.EXC_RETURN or retVal == self.EXC_RAISE or retVal == self.EXC_RAW:
            
            if className != None:
                ARGS = self.ClassXHandler(className)
            else:
                ARGS = self.FunctionXHandler(retVal)
      
        if logMsg !="":
            ARGS["Message"] = logMsg
            
        if self.Debug:
            print ARGS["Message"]
                      
        if logEvent:
            self.LogEvent(ARGS)
                    
        if retVal == self.EXC_RAISE:
            raise
        elif retVal == self.EXC_RAW:
            return ARGS
        
        return retVal
     
     
   
    
    def LogEvent(self, ARGS):
        try:  
            if  self.LOG_OBJ != None:
                #logging object
                self.LOG_OBJ(ARGS["Message"])
            
     
            elif self.LOG_OBJ == None:
                #default log 
                LogPath = self.LOG_PATH+self.LOG_FILE
                if not os.path.exists(LogPath):
                    os.mkdir(LogPath)
                fp = open(LogPath, "a+")
                fp.write(ARGS["Message"])
                fp.close()
          
        except:
            return self.ClassXHandler(self.xname)
        
            
            
   
       


 
if __name__ == '__main__':       
            
    ############################################################################
    #Simple Setup To Show How To Reuse Your Already Instantiated Logging 
    #Xceptions.py to override the default internal log
    import logging
    logging.basicConfig(filename="ProjectLog.txt",level=logging.DEBUG) 
    Log_Object = logging.debug
    
   
            
    ##########################################################################
    # Function Usage Example
    
    XH =XceptionHandler(DEBUG=True, LOG_TABLE="DBLogTable", 
                        LOG_OBJ=Log_Object, LOG_EVENTS=True)
    
    def _Return(*args):
        return XH.ProcessReturn(None, args)
    
    
    def XampleFunction1():
        try:
            x = 2/0
            return _Return(1, "SUCCESS")
        except:
            tb_dump = _Return(-2)
            print tb_dump
            return tb_dump
            
     
    def XampleFunction2():
        try:
            x = 2/0
            return _Return(1, "SUCCESS", False) #override LOG_EVENTS one time
        except:
            return _Return(-1)
        
     
    def XampleFunction3():
        try:
            x = 2/1
            return _Return(1, "SUCCESS")
        except:
            _Return(-3)
        
    ############################################################################
    
    ############################################################################
    # Class Usage Example
    
    class XampleClass(XceptionHandler):
    
       def __init__(self):
            self.name       = str(self.__class__).split(".")[1]
            XceptionHandler.__init__(self, DEBUG=True, LOG_EVENTS=False)
           
       def _Return(self, *args):
           return self.ProcessReturn(self.name, args)
       
       def Test1(self):
           try:
               print x
               return self._Return(1)
           except:
               return self._Return(-1)
           
       def Test2(self):
           try:
               print z
               return self._Return(True, "Success")
           except:
               return self._Return(-1, "FAIL", True)
              
       def Test3(self):
           try:
               print w
               return self._Return(True, "Success")
           except:
               return self._Return(-2, "FAIL returning traceback dump")
           
       def Test4(self):
           try:
               print w
               return self._Return(True, "Success")
           except:
               self._Return(-3)
           
    ############################################################################  
  
    
    XampleFunction1()
    XampleFunction2()
    XampleFunction3()
    
    xc = XampleClass()
    xc.Test1()
    xc.Test2()
    xc.Test3()
    xc.Test4()
    
    
              

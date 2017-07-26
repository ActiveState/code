import sys, thread
from array import array
from Xceptions import XceptionHandler


"""
PluginManager

Author: AJ Mayorga
Date:   5/5/2010

** Here Module and Plugin are used interchangably to refer to custom
   code provided during runtime of a project to provide additional 
   functionality. Not the import of a proper Python module **


A Demo And Framework For Creating Plugins/Modules For Python Projects. 
Providing For:

    - Modules contain there own pragma section for config vars

    - Pragma sections are read and validated by Preparser before evaluating/executing
          - Checks for necessary config vars
          - Checks module dependencies

    - Modules can be run inline or inside of their own thread

    - Provides for module garbage collection
 

"""

#Some Constants For Use with Xceptions
EXC_RETURN = -1 # Report Exception and return ie continue on
EXC_RAW    = -2 # Report on and return a traceback dump as dict() then continue
EXC_RAISE  = -3 # Report on & raise the exception do not continue 


########################################################
# Thanks to Daniel Brodie for the how to on Extending Classes
# http://code.activestate.com/recipes/412717

def get_obj(name): return eval(name)

class ExtendInplace(type):
    def __new__(self, name, bases, dict):
        prevclass = get_obj(name)
      
        del dict['__module__']
        del dict['__metaclass__']

       
        for k,v in dict.iteritems():
            setattr(prevclass, k, v)
        return prevclass

########################################################

"""
Exception Class For Our Preparser
we'll use this when we want to raise on a
logic failure

"""
class ModuleParserException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)


"""
Reading in the Pragma Section from the Module get config parameters
Ensure Module has needed parameters and check module dependencies


"""
class Preparser(XceptionHandler):
    def __init__(self):
        self.name        = str(self.__class__).split(".")[1]
        XceptionHandler.__init__(self, DEBUG=False)
        
        #Modules Are Required To Have These Config Parameters
        self.params = ['_NAME_','_AUTHOR_','_DATE_','_DEPENDS_','_ON_EXC_','_RUN_']
    
    
    def Parser_Xception(self, *args):
        return self.ProcessReturn(self.name, args)
    
    
    def DependencyCheck(self, Modules):
        try:
            depends     =  list()
            ModuleNames =  [Module['_NAME_'] for Module in Modules]
          
            for Module in Modules:
                count = 0
                for d in Module['_DEPENDS_']:
                    if not d in ModuleNames:
                        msg  = "MODULE: "+Module['_NAME_']+" Failed Dependency Check"
                        msg += " Dependency "+d+" Could Not Be Found"
                        raise ModuleParserException(msg)
        except:
            self.Parser_Xception(EXC_RAISE)
        
        
    def LoadModules(self, Modules):
        ModulesOut = list()
        try:
            for Module in Modules:
                Module = self.ProcessModule(Module)
                ModulesOut.append(Module)
                
            self.DependencyCheck(ModulesOut)
            
            for Module in ModulesOut:
                yield Module
            
        except:
            self.Parser_Xception(EXC_RAISE)
        
        
    def ProcessModule(self, Module):
        try:
            ModuleOut   = dict()
            StartTag    = "PRAGMA_START"
            EndTag      = "PRAGMA_END"
            
            pragma_section = Module[Module.find(StartTag)+len(StartTag):Module.rfind(EndTag)-1].strip()
            args = pragma_section.split('\n')
            for x in args:
                key, value = x.split('=')
               
                key   = key.replace(" ", "")
                key   = key.replace("self.", "")
                value = value.replace(" ", "")
                
                ModuleOut[key] = eval(value)
            
            ModuleOut['CODE'] = Module
            moduleName        = ModuleOut.get('_NAME_', "Unknown")
            for param in self.params:
                if not ModuleOut.has_key(param):
                    raise ModuleParserException("MODULE: "+moduleName+" PRAGMA SECTION IS MISSING: "+param)
                    
            return ModuleOut
           
        except:
            self.Parser_Xception(EXC_RAISE)
          

"""
Plugin/Module Manager Class, All modules will run as an extention of this class

"""        
class ModuleAPI(XceptionHandler, Preparser):
    def __init__(self):
        self.name        = str(self.__class__).split(".")[1]
        XceptionHandler.__init__(self, DEBUG=False)
        Preparser.__init__(self)
        
        """
        These vars the the only intended vars meant to survive module runs
        other objects created by the module will be cleaned up after run

        """
        self.ModuleARGS             = None
        self.ModuleName             = ""
        self.ModuleDataStor         = None
        self.ModuleReturn           = None
        self.ModuleXceptionHandler  = XceptionHandler(DEBUG=True)
        self.ModuleOnException      = ""
        
        self.OrigObjects            = None
        
     
    def ModuleAPI_Xception(self, *args):
        return self.ProcessReturn(self.name, args)
    
    
    def ModuleXception(self, *args):
        return self.ModuleXceptionHandler.ProcessReturn(self.ModuleName, args)

       
    """
    Really this is a place holder, just printing, but can be called from within the module
    to relay messages to DB,Server,Parent Process etc.

    """    
    def Callback(self, Message):
        print Message

        
    """
    Here we check to see what objects have been created during our module run
    and delete them garbage collection of sorts.
    This helps with object naming issues between modules, conserving resources etc.

    """        
    def CleanUp(self):
        cleanup = list()
                   
        for k, v in self.__dict__.iteritems():
            if  not self.OrigObjects.has_key(k):
                cleanup.append(k)
                        
        for old in cleanup:
            del self.__dict__[old]
            
            
    """
    Where we bring it all together

    """
    def RunModules(self, Modules, Args):
        ret = True
        self.OrigObjects   = self.__dict__.copy()
        
        for Module in self.LoadModules(Modules):
            try:        
                self.ModuleName        = Module['_NAME_']
                self.ModuleOnException = Module['_ON_EXC_']
                self.ModuleARGS        = Args
                
                print "STARTING NEW MODULE RUN:  ",self.ModuleName,"\n"
                
                eval(compile(Module['CODE'], sys.argv[0], "exec"))
                
                if   Module['_RUN_'] == 'INLINE':
                     self.Run()
                    
                elif Module['_RUN_'] == 'THREAD':
                     self.lock=thread.allocate_lock()
                     self.lock.acquire()
                     thread.start_new_thread ( self.Run, () )
                     self.lock.acquire()
                    
                self.Callback(self.ModuleName+" Output:"+self.ModuleDataStor.tostring()+"\n")
                
            except:
                self.Callback(self.ModuleAPI_Xception(self.ModuleOnException))
                ret = False
                break
            finally: 
                self.ModuleARGS = None
                self.CleanUp()
              
                
                print "ENDING MODULE RUN:  ",self.ModuleName,"\n\n"
                 
        return ret
    




Module1 = """

class ModuleAPI:

    __metaclass__   = ExtendInplace
    
    def Init(self):
        try:
            __name__        = self.ModuleName
          
            #PRAGMA_START

            self._NAME_           = 'VModule_Test1'
            self._AUTHOR_         = 'AJ Mayorga'
            self._DATE_           = 'May 1, 2010'
            self._DESCRIPTION_    = 'Test Plugin'
            self._DEPENDS_        = ()
            self._ON_EXC_         =  EXC_RETURN
            self._RUN_            = 'INLINE'

            #PRAGMA_END
            
            if self.ModuleDataStor:
                self.DataBuffer   = self.ModuleDataStor
            else:
                self.DataBuffer   = self.ModuleARGS['DataBuffer']
                
            self.Return           = False

        except:
            self.ModuleXception(self._ON_EXC_)
   
   
    def Run(self):
        try:
            self.Init()
            self.Callback(self.ModuleName+" Input: "+self.DataBuffer.tostring())
            self.ModData()
            self.ModuleDataStor  = self.DataBuffer
            self.Return = True
            
        except:
            self.ModuleDataStor = self.ModuleARGS['DataBuffer']
            self.ModuleXception(self._ON_EXC_)
            
        finally:
            self.ModuleReturn = self.Return
            if self._RUN_ == 'THREAD':
                print self.ModuleName,"Exiting From Thread: ",thread.get_ident()
                lock.release()
         
           
    def ModData(self):
        try:
            import string
            temp = self.DataBuffer.tostring()
            temp = string.replace(temp, "SCARY", "HAPPY")
            self.DataBuffer = array('B', temp)
            
        except:
            return self.ModuleXception(self._ON_EXC_)
    
"""


       
Module2 = """

class ModuleAPI:
    
    __metaclass__   = ExtendInplace
    
    def Init(self):
        try:
            __name__        = self.ModuleName
                   
            #PRAGMA_START

            self._NAME_           = 'VModule_Test2'
            self._AUTHOR_         = 'AJ Mayorga'
            self._DATE_           = 'May 1, 2010'
            self._DESCRIPTION_    = 'Test Plugin'
            self._DEPENDS_        = ('VModule_Test1', 'VModule_Test3')
            self._ON_EXC_         =  EXC_RETURN
            self._RUN_            = 'THREAD'

            #PRAGMA_END
             
            if self.ModuleDataStor:
                self.DataBuffer   = self.ModuleDataStor
            else:
                self.DataBuffer   = self.ModuleARGS['DataBuffer'] 

            self.Return           = False
            
        except:
            self.ModuleXception(self._ON_EXC_)
   
   
    def Run(self):
        try:
            self.Init()
            self.Callback(self.ModuleName+" Input: "+self.DataBuffer.tostring())
            self.ModData()
            self.ModuleDataStor = self.DataBuffer
            self.Return = True
            
        except:
            self.ModuleDataStor = self.ModuleARGS['DataBuffer']
            self.ModuleXception(self._ON_EXC_)
            
        finally:
            self.ModuleReturn = self.Return
            if self._RUN_ == 'THREAD':
                print self.ModuleName,"Exiting From Thread: ",thread.get_ident()
                self.lock.release()
       
           
    def ModData(self):
        try:
            import string
            temp = self.DataBuffer.tostring()
            temp = string.replace(temp, "RECTAL", "LITTLE")
            self.DataBuffer = array('B', temp)
        except:
            return self.ModuleXception(self._ON_EXC_)

"""


       
Module3 = """

class ModuleAPI:
    
    __metaclass__   = ExtendInplace
    
    def Init(self):
        try:
            __name__        = self.ModuleName
                   
            #PRAGMA_START

            self._NAME_           = 'VModule_Test3'
            self._AUTHOR_         = 'AJ Mayorga'
            self._DATE_           = 'May 1, 2010'
            self._DESCRIPTION_    = 'Test Plugin'
            self._DEPENDS_        = ('VModule_Test1', 'VModule_Test2')
            self._ON_EXC_         =  EXC_RETURN
            self._RUN_            = 'INLINE'

            #PRAGMA_END
           
            if self.ModuleDataStor:
                self.DataBuffer   = self.ModuleDataStor
            else:
                self.DataBuffer   =  self.ModuleARGS['DataBuffer'] 

            self.Return           = False
            
        except:
            self.ModuleXception(EXC_RETURN)
   
   
    def Run(self):
        try:
            self.Init()
            self.Callback(self.ModuleName+" Input: "+self.DataBuffer.tostring())
            self.ModData()
            self.ModuleDataStor = self.DataBuffer
            self.Return = True
            
        except:
            self.ModuleDataStor = self.ModuleARGS['DataBuffer']
            self.ModuleXception(self._ON_EXC_)
            
        finally:
            self.ModuleReturn = self.Return
            if self._RUN_ == 'THREAD':
                print self.ModuleName," Exiting From Thread: ",thread.get_ident()
                lock.release()
          
    def ModData(self):
        try:
            import string
            temp = self.DataBuffer.tostring()
            temp = string.replace(temp, "THERMOMETERS", "TREES")
            self.DataBuffer = array('B', temp)
        except:
            return self.ModuleXception(EXC_RAISE)
    
"""

    
    
if __name__ == '__main__':       
               
    Modules                = [Module1, Module2, Module3]
    ARGS                   = dict()
    ARGS['DataBuffer']     = array('B', "SCARY RECTAL THERMOMETERS")
    
    
    ModAPI = ModuleAPI()
    
    #Call One
    print "Running One Module"
    ModAPI.RunModules([Module1], ARGS)
    print "Single Module Output: ", ModAPI.ModuleDataStor.tostring()
    
    print "\n\n"
    
    #Call Them All
    print "Running All Modules"
    ModAPI.RunModules(Modules, ARGS)
    
    print "Module Group Output:  ",ModAPI.ModuleDataStor.tostring()
    
    
    
    
    

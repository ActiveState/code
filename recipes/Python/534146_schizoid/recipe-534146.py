###############################################################################

import inspect, new, sys

registry = {}

# master registry for methodnames, decorators, and proxy scope dummy object
###############################################################################

class proxy(object): pass

def personalityDependant(func):
   """ we have to save func in the registry so each duplicate 
            function name doesnt just overwrite the previous one 
   
            NOTE: "whichSelf" is the name of the variable used where 
                  "self" is usually found in instancemethod definitions
   """
   whichSelf = inspect.getargspec(func)[0][0]  
   if whichSelf not in registry:	registry[whichSelf] = {}
   registry[whichSelf][func.__name__] = func		
   return func	

def schizophrenic(func):
   """ tag a function as schizophrenic so the metaclass knows when to 
      effect the scope mangling. """
   func.schizophrenic=True
   return func

# metaclass for all schizoids
###############################################################################

class schizotypal(type):		
   """ """
   @staticmethod
   def __new__(mcls, name, bases, clsdict):
      err1 ='expected a schizotypal object would have a list of personalities.'
      try:			assert 'personalities' in clsdict
      except AssertionError:	raise Exception, err1
      else:			
            personalities = clsdict['personalities']
            replacement   = {}
            for pName in personalities: replacement[pName] = registry[pName]
            personalities = replacement
            clsdict['personalities'] = personalities
            klassobj = type.__new__(mcls, name, bases, clsdict)
      return klassobj
	
   def __call__(cls, *args, **kargs):
      inst = type.__call__(cls, *args, **kargs)
      for var in dir(inst):
            val  = getattr(inst, var)
            test = var!='__metaclass__' and var!='__class__'
            if hasattr(val, 'schizophrenic') and test:
               for pName in inst.personalities:
                        val.func_globals[pName] = inst.as(pName)
      return inst

# base schizoid object (inherit from this)
###############################################################################

class schizoid(object):
   """ """		
   __metaclass__ = schizotypal
   personalities = []
   
   def as(self, pName):
      """ obtain a representation of self with respect to some personality """
      cls = self.__class__
      err = 'illegal personality for '+str(cls) + ': ' + pName
      assert pName in cls.personalities, err
      out   = cls.personalities[pName]
      P = proxy()
      for funcname in out:
            func = out[funcname]
            func = new.instancemethod(func,self,cls)
            setattr(P, funcname, func)
      return P
			
# a demo
###############################################################################

class myschizoid(schizoid):		
   """ a simple demo.

      note that without the decorators, each status() definition would simply
      overwrite the previous one.  notice also under normal python semantics
      how theres no reason the philosopher names in the run() method should 
      be in scope.
   """
   personalities = ['kant','heidegger','wittgenstein','schlegel']
   
   @personalityDependant
   def status(kant):          return "a real pissant"
   
   @personalityDependant 
   def status(heidegger):     return "a boozy beggar" 
   
   @personalityDependant 
   def status(wittgenstein):  return "beery swine"
   
   @personalityDependant 
   def status(schlegel):      return "schloshed"
   
   @schizophrenic
   def run(self):
      print
      print 'kant:\t\t\t',		kant.status()
      print 'heidegger:\t\t',		heidegger.status()
      print 'wittgenstein:\t\t',	wittgenstein.status()
      print 'schlegel:\t\t',		schlegel.status()
      print

if __name__=='__main__':		
	s = myschizoid()
	s.run()

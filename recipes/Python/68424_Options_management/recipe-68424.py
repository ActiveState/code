class OptionError (AttributeError):	
    pass
	
class OptionsUser:	
	""" This class is intended to be used as a base class for class that	need to use Options"""
	def initOptions (self,option, kw):
		"""Method intended to be called from the derived class constructor.
		   Put the options into object scope."""
		for k,v in option.__dict__.items()+kw.items():
			if not hasattr(self.__class__,k):
				raise OptionError,"invalid option "+k
			setattr(self,k,v)
	
	def reconfigure(self,option=Options(), **kw):
		""" Public member that should be used to change options during object life"""
		self.InitOptions(option,kw)
		self.onReconfigure(self)
		
	def onReconfigure(self):
		""" Public member intended to be overloaded by derived class. Called by
		    reconfigure method but can also be called from the output in case of
		    direct access to options attributs"""
		pass
		

class Options:
	def __init__(self, **kw):
		self.__dict__.update(kw)
		
	def __lshift__(self,other):
		"""overloading operator """
		s = self.__copy__()
		s.__dict__.update(other.__dict__)
		return s
		
	def __copy__(self):
		s = self.__class__()
		s.__dict__ = self.__dict__.copy()
		return s
			

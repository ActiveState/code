def _curry(fn, *cargs, **ckwargs):
    def call_fn(*fargs, **fkwargs):
        d = ckwargs.copy()
        d.update(fkwargs)
        return fn(*(cargs + fargs), **d)
    return call_fn

class MultiHandler(ContentHandler, object):
   """
   MultiHandler is a handler for the xml.sax parser.
   Its purpose is to dispatch calls to one or more other handlers.
   When dealing with really large XML files (say, Wikipedia's 100GB full text dump)
   this is handy so that you can process the information in multiple (modular) ways
   without having to read the whole file off disk in separate passes.
   
   If an exception is thrown from a constituent handler call, MultiHandler will 
      dump a diagnostic to the supplied errout (or stderr) 
      and continue processing.
      
   Example usage:
      import sys
      from xml.sax import make_parser
      from xml.sax.handler import feature_namespaces, ContentHandler
      from MultiHandler import MultiHandler
   
      mh = MultiHandler()
      mh.handlers.append(YourHandler())
      mh.handlers.append(YourOtherHandler())
      parser = make_parser()
      parser.setFeature(feature_namespaces, 0)
      parser.setContentHandler(mh)
      parser.parse(sys.stdin)   
   """
   #ContentHandler is just inherited to make isinstance happy.  
   #we'll be overridding everything using new-style __getattribute__.
   def __init__(self, errout=None):
      self.handlers = []
      self.errout = errout
      if self.errout == None:
         import sys
         self.errout = sys.stderr
   
   def __getattribute__(self, name):
      if name == 'handlers' or name == 'errout':
         return object.__getattribute__(self, name)
      def handlerCall(self, *args, **kwargs):
         for handler in self.handlers:
            try:
               m = getattr(handler, name)
               m(*args, **kwargs)
            except:
               self.errout.write('MultiHandler: error dispatching %s to handler %s\n' %  \
                     (name, str(handler)))
   
      ret = _curry(handlerCall, self)
      return ret

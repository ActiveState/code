from pyparsing import *

class PyparsingProcessor(object):
    def __init__(self):
        self._identifiers = {}
       
    def __getitem__(self, key):
        try:
            return self._context[key]
        except KeyError:
            if self._identifiers.has_key(key):
                return self._identifiers[key]
            self._identifiers[key] = Forward()
            return self._identifiers[key]
   
    def __setitem__(self, key, value):
        try:
            self._identifiers[key] << value
            self._context[key] = self._identifiers[key]
        except Exception, e:
            self._context[key] = value
       
    def ProcessPyparsingModule(self, iterable, context):
        self._context = context
        exec iterable in context, self

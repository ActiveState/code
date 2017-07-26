'''
jsonextensions

Author : Michael Palmer


This package was created to provide a flexible, configurable, and maintainable way to customize json input and output. 

The concept behind the package is to build a single class per type you want to add to json. The new class will have a method for encoding to json and a method
for decoding from json. The classes are then loaded into an encoder object and a decoder object that are hooked into the standard json loads
and dumps functions.

Encoding depends on recognizing the type of the object to be encoded when encountered in a Python object being converted into JSON format. Decoding depends on
recognizing the display name of the custom encoded JSON object. Each JSON extension class thus has two attributes to control encoding and decoding - addedtype 
for encoding and displayname for decoding. 


Tested With: Python 2.7, 3.4

Sample Usage:

>>> from jsonextensions import *
>>> configure_extensions(JSONSet(),JSONDateTime(),JSONDecimal())
>>> a = { 1.7, True, 'Apple'}
>>> jsonset = writeJSON(a)
>>> jsonset
'{"__set__": "true", "values": [true, 1.7, "Apple"]}'
>>> jsonobj = readJSON(jsonset)
>>> jsonobj
{True, 1.7, 'Apple'}

'''

import json
from   datetime import datetime
from   decimal  import Decimal
from   collections import OrderedDict

DEFAULT_TIME_FMT = "%Y-%m-%d %H:%M:%S:%f"

def writeJSON(obj):
    """
       A simple convenience function to illustrate the extended conversion of Python objects to JSON. configure_extensions must be called with added types to make this function 
       useful.
       
    """
    return json.dumps(obj,cls=EnhancedJSONEncoder)

def readJSON(jsonobj):
    """
      A simple convenience function to illustrate the conversion of custom JSON objects into Python. configure_extensions must be called with added types to make this funciton 
      useful.
      
    """
    return json.loads(jsonobj,object_hook = (EnhancedJSONDecoder()).decode)

def configure_extensions(*args):
    """
        A convenience function to initialize the extended JSON encoder and decoder classes.
        
        Example Usage:
        >>> configure_extensions(JSONSet(),JSONDateTime(),JSONDecimal())
        
        Args:
          *args    : A variable list of arguments that comprise JSON extension classes. 
    """
    EnhancedJSONEncoder.addtypes(*args)
    EnhancedJSONDecoder.addtypes(*args)

class EnhancedJSONEncoder(json.JSONEncoder):
    """
     EnhancedJSONEncoder provides a way to render non-JSON compatible Python objects in JSON. When a registered non-standard object is encountered in
     the Python object being converted to JSON the custom encode function is called to render the object as a JSON string.
     
     Usage: (Assumes the EnhancedJSONEncoder has been configured - see configure_extensions())
     >>> jsonobj = json.dumps(obj,cls=EnhancedJSONEncoder)
     
    """
    addedtypes = {}
    @classmethod
    def addtypes(cls,*additions):
        for x in additions:
            cls.addedtypes[x.addedtype] = x
    def default(self, obj):
        if type(obj) in self.addedtypes:
            return self.addedtypes[type(obj)].encode(obj) 
        return json.JSONEncoder.default(self, obj)
    
class EnhancedJSONDecoder(object):
    """
     EnhancedJSONDecoder provides a way to instantiate non-JSON compatible Python objects from specially structured JSON code.  When the text for a 
     registered non-standard object is encountered in the JSON text the custom decode function is called to convert the string into a Python object.
     
     Usage: (Assumes the EnhancedJSONDecoder has been configured - see configure_extensions())
     >>> pyobj = json.loads(obj,object_hook = self.EnhancedJSONDecoder.decode)
     
    """
    addedtypes = {}
    @classmethod
    def addtypes(cls,*additions):
        for x in additions:
            cls.addedtypes[x.displayname] = x
    def decode(self,dct):
        for t in self.addedtypes.keys():
            if t in dct:
                return self.addedtypes[t].decode(dct)
        return dct
    
class JSONDecimal(object):
    """
        The JSONDecimal class provides a JSON extension to code the Decimal object from the decimal module.
        
        Usage:
        >>> configure_extensions(JSONSet(),JSONDateTime(),JSONDecimal())  
        >>> a = Decimal("11.9")
        >>> s = json.dumps(a,cls=EnhancedJSONEncoder)
        >>> s
        '{"__Decimal__": "true", "value": "11.9"}'
        >>> l = json.loads(s,object_hook=(EnhancedJSONDecoder()).decode)
        >>> l
        Decimal('11.9')
    """
    def __init__(self):
        self.addedtype   = Decimal
        self.displayname = '__Decimal__'
        self.valuename   = 'value'
    def encode(self,obj):
        if type(obj) == self.addedtype:
            return OrderedDict([( self.displayname,"true"),(self.valuename,str(obj))])
    def decode(self,dct):
        if self.displayname in dct:
            return Decimal(dct[self.valuename])
        return dct
    
class JSONSet(object):
        """
            The JSONSet class provides a JSON extension to code the built-in set object.
            
            ***Note: Python's default set is unordered. A test on set order will fail***
         
        Usage: 
        >>> configure_extensions(JSONSet(),JSONDateTime(),JSONDecimal())  
        >>> a = set([1,2,3])
        >>> s = json.dumps(a,cls=EnhancedJSONEncoder)
        >>> s
        '{"__set__": "true", "values": [1, 2, 3]}'
        >>> l = json.loads(s,object_hook=(EnhancedJSONDecoder()).decode)
        >>> l
        {1, 2, 3}
            
        """
        def __init__(self):
            self.addedtype   = set
            self.displayname = '__set__'
            self.valuename   = 'values'
        def encode(self,obj):
            if type(obj) == self.addedtype:
                return OrderedDict([(self.displayname,"true"),(self.valuename,list(obj))])
        def decode(self,dct):
            if self.displayname in dct:
                return set(dct[self.valuename])
            return dct

class JSONDateTime(object):
        """
            The JSONDateTime class provides a JSON extension for the datetime object from the datetime module.
        
        Usage:
        >>> a = datetime.today()
        >>> s = json.dumps(a,cls=EnhancedJSONEncoder)
        >>> s
        '{"format": "%Y-%m-%d %H:%M:%S:%f", "__datetime__": true, "value": "2015-07-12 21:03:42:081334"}'    
        >>> l = json.loads(s,object_hook=(EnhancedJSONDecoder()).decode)
        >>> l
        datetime.datetime(2016, 5, 21, 18, 10, 22, 584945)
        
        """
        def __init__(self,timefmt=DEFAULT_TIME_FMT):
            self.addedtype   = datetime
            self.displayname = '__datetime__'
            self.valuename   = 'value'
            self.formatname  = 'format'
            self.timefmt     = timefmt 
        def encode(self,obj):
            if type(obj) == self.addedtype:
                return OrderedDict( [(self.displayname,True),(self.formatname,self.timefmt),(self.valuename,obj.strftime(self.timefmt))])
        def decode(self,dct):
            if self.displayname in dct:
                return datetime.strptime(dct[self.valuename], dct[self.formatname]) 


            

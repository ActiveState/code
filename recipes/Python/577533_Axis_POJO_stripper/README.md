## Axis POJO stripper.  
Originally published: 2011-01-04 12:05:02  
Last updated: 2011-01-04 12:05:12  
Author: Chris Wolf  
  
This utility lets us use the 'wsdl2java' utility from Axis-1 to 
generate POJOs from the schema embedded in a WSDL.  If we just want
POJOs without the Axis marshalling/unmarshalling code, then this
script will strip out the Axis code, leaving just the POJOs.
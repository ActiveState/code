## Unicode class which adds proper XML declaration on encoding 
Originally published: 2007-08-09 04:52:45 
Last updated: 2007-08-09 04:52:45 
Author: Dmitry Vasiliev 
 
Sometimes you want to pass XML document as unicode object which later should be encoded for output. Unfortunately very often you don't know the output encoding and can't set XML declaration properly. UnicodeXML adds XML declaration right on encoding operation.
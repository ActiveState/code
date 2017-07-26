## DoDefaultMixin 
Originally published: 2004-04-22 12:30:10 
Last updated: 2004-04-22 20:04:19 
Author: Paul McNett 
 
Simple recipe for making it easier to call superclass method code. Instead of 'super(cls,self).methodName()' you may just use 'cls.doDefault()' for code that is easier on the eyes.
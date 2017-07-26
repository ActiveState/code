## SAX to DOM ChunkerOriginally published: 2004-08-06 08:48:59 
Last updated: 2004-08-06 08:48:59 
Author: Uche Ogbuji 
 
This module is similar to pulldom in that it takes a stream of SAX objects and breaks it down into chunks of DOM.  The differences are that it works with any DOM implementation meeting the Python DOM conventions, and that it uses simple pattern expressions to declaratively set how the DOM chunks are partitioned, rather than requiring the user to write procedural code for this purpose.  This is an updated/fixed version of code that appeared in an XML.com column.
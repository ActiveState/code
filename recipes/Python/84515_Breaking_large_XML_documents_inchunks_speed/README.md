## Breaking large XML documents into chunks to speed processing  
Originally published: 2001-10-31 12:56:39  
Last updated: 2001-10-31 12:56:39  
Author: Mike Hostetler  
  
One of the few problems with using Python to process XML is the speed -- if the XML becomes somewhat large (>1Mb), it slows down exponentially as the size of the XML increases.  One way to increase the processing speed is to break the XML down via tag name.  This is especially handy if you are only interested in one part of the XML, or between certain elements throughout the XML.\n\nHere is a function that I came up with to handle this problem -- I call it "tinyDom".  It uses the Sax reader from PyXML, although it could be easily changed for minidom, etc.\n\nThe In parameters are the XML as a string, the tag name that you want to build the DOM around, and an optional postition to start at within the XML.  It returns a DOM tree and the character position that it stopped at.
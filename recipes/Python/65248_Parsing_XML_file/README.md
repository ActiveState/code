## Parsing an XML file with xml.parsers.expat 
Originally published: 2001-06-19 10:34:54 
Last updated: 2001-07-27 15:31:46 
Author: Mark Nenadov 
 
This is a reusable way to use "xml.parsers.expat" to parse an XML file. When re-using the "MyXML" class, all you need to define a new class, with "MyXML" as the parent. Once you have done that, all you have to do is overwrite the inherited XML handlers and you are ready to go.
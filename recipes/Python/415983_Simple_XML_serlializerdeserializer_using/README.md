## Simple XML serlializer/de-serializer using Python dictionaries and marshalling

Originally published: 2005-06-03 12:59:49
Last updated: 2005-06-07 09:13:40
Author: Anand 

This recipe presents a way of serializing & de-serializing XML using\nthe marshal module. The XML is converted to an equivalent Python\ndictionary first, which is marshaled to serialize it. De-serialization\nfirst unmarshals the dictionary from the file, and constructs the\noriginal XML.
## Simple XML serlializer/de-serializer using Python dictionaries and marshalling  
Originally published: 2005-06-03 12:59:49  
Last updated: 2005-06-07 09:13:40  
Author: Anand   
  
This recipe presents a way of serializing & de-serializing XML using
the marshal module. The XML is converted to an equivalent Python
dictionary first, which is marshaled to serialize it. De-serialization
first unmarshals the dictionary from the file, and constructs the
original XML.
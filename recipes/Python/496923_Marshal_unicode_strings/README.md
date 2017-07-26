## Marshal unicode strings with PyXML

Originally published: 2006-07-28 06:49:00
Last updated: 2006-07-28 06:49:00
Author: Alex Greif

If you want to serialize Python objects to XML then PyXML is a good choice. Except in the case when unicode strings come into play. In this case generic.Marshaller().dump() throws an ugly AttributeError: Marshaller instance has no attribute 'm_unicode'\nThis recipe extends both PyXML Marshaller and Unmarshaller to support the de-/serialization of unicode strings. Put the following code in a separate module and test it with the given example.\nThe output will look like\n&lt;marshal&gt;\n&nbsp;&nbsp;&lt;list id="i2"&gt;\n&nbsp;&nbsp;&nbsp;&nbsp;&lt;string&gt;text&lt;/string&gt;\n&nbsp;&nbsp;&nbsp;&nbsp;&lt;unicode>german umlaut: ü ö <>&&lt;/unicode&gt;\n&nbsp;&nbsp;&lt;/list&gt;\n&lt;/marshal&gt;
## Detect character encoding in an XML file  
Originally published: 2005-01-19 16:35:10  
Last updated: 2005-01-20 00:50:37  
Author: Lars Tiede  
  
A function analyzing an open xml file for its character encoding by\n- checking for a unicode BOM or (on failure)\n- searching the xml declaration at the beginning of the file for the "encoding" attribute
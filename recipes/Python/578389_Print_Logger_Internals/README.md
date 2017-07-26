## Print Logger Internals  
Originally published: 2012-12-24 04:11:32  
Last updated: 2012-12-24 04:11:35  
Author: Dave Bailey  
  
This helper function simplifies the difficult task of setting up and maintaining a logging system. Changes to a logging system can cause unanticipated consequences such as lost messages or duplicates. Debugging a logging hierarchy can be a tedious task. This function overrides the internal __repr__ functions of the internal classes and allows a print statement to generate the complete logger hierarchy with its associated internals. It allows easy debugging a logger and allows changes to be easily detected.\n
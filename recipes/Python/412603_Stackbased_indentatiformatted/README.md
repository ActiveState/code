## Stack-based indentation of formatted logging 
Originally published: 2005-04-28 16:13:06 
Last updated: 2005-04-28 23:27:16 
Author: Christopher Dunn 
 
Some people like to sprinkle stack trace information in their code, and it is always helpful to get a visual clue to the call stack depth. inspect.stack() contains the entire call stack.\n\nTo make this information available conditionally, on a per-subsystem basis, the logging module is helpful. Here is one way to combine the two ideas.
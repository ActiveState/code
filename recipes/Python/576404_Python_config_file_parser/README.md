## Python config file parser  
Originally published: 2008-08-02 12:55:21  
Last updated: 2008-08-02 12:55:21  
Author: Frithiof andreas Jensen  
  
Config - reads a configuration file.

This module parses a configuration file using a restricted Python syntax.
The Python tokenizer/parser is used to read the file, unwanted expressions
are removed from the parser output before the result is compiled and
executed. The initialised configuration settings are returned in a dict.



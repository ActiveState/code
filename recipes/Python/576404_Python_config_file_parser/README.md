## Python config file parser  
Originally published: 2008-08-02 12:55:21  
Last updated: 2008-08-02 12:55:21  
Author: Frithiof andreas Jensen  
  
Config - reads a configuration file.\n\nThis module parses a configuration file using a restricted Python syntax.\nThe Python tokenizer/parser is used to read the file, unwanted expressions\nare removed from the parser output before the result is compiled and\nexecuted. The initialised configuration settings are returned in a dict.\n\n\n
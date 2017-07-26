## Persistent dict with multiple standard file formats  
Originally published: 2009-02-04 01:08:27  
Last updated: 2011-09-06 20:01:46  
Author: Raymond Hettinger  
  
dbdict: a dbm based on a dict subclass.\n\nOn open, loads full file into memory.\nOn close, writes full dict to disk (atomically).\nSupported output file formats: csv, json, and pickle.\nInput file format automatically discovered.\n\nUsable by the shelve module for fast access.
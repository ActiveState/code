## Persistent dict with multiple standard file formats  
Originally published: 2009-02-04 01:08:27  
Last updated: 2011-09-06 20:01:46  
Author: Raymond Hettinger  
  
dbdict: a dbm based on a dict subclass.

On open, loads full file into memory.
On close, writes full dict to disk (atomically).
Supported output file formats: csv, json, and pickle.
Input file format automatically discovered.

Usable by the shelve module for fast access.
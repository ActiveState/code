## easyjson.py - parsing JSON from buffer and from file  
Originally published: 2013-05-24 04:09:07  
Last updated: 2013-05-27 05:32:07  
Author: Thomas Lehmann  
  
**JSON Parser**:
 * Refering to http://www.json.org/
 * Just one simple Python file you can integrate where you want to
 * No imports (very important) -> no dependencies!!!
 * Should work with really older versions of Python!!!

**Todo's**:
 * Doesn't cover full number format
 * ...

**Done**
 * Allows string in string (revision 2)
 * Covers objects in an array (revision 2)
 * Provides a mechanism to allow other dictionaries (like collections.OrderedDict) (revision 3)
 * Conversion of numbers to integer or float types (revision 4)

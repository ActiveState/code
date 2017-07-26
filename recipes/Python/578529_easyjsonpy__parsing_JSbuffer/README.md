## easyjson.py - parsing JSON from buffer and from file 
Originally published: 2013-05-24 04:09:07 
Last updated: 2013-05-27 05:32:07 
Author: Thomas Lehmann 
 
**JSON Parser**:\n * Refering to http://www.json.org/\n * Just one simple Python file you can integrate where you want to\n * No imports (very important) -> no dependencies!!!\n * Should work with really older versions of Python!!!\n\n**Todo's**:\n * Doesn't cover full number format\n * ...\n\n**Done**\n * Allows string in string (revision 2)\n * Covers objects in an array (revision 2)\n * Provides a mechanism to allow other dictionaries (like collections.OrderedDict) (revision 3)\n * Conversion of numbers to integer or float types (revision 4)\n
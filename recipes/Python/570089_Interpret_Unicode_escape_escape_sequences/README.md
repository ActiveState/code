## Interpret Unicode escape escape sequences written to stdout and stderrOriginally published: 2008-04-16 07:33:05 
Last updated: 2008-04-16 14:47:48 
Author: Nick Coghlan 
 
Python 2.6 and 3.0 make it practical to implicitly convert hexadecimal Unicode escape sequences sent to stdout or stderr (or other text files) back to the original Unicode characters.
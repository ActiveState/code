## Merging XBEL Bookmark files 
Originally published: 2002-06-23 14:46:14 
Last updated: 2002-06-23 14:46:14 
Author: Uche Ogbuji 
 
This recipe uses DOM (precisely, cDomlette or the minidom variant in 4Suite) to merge two files containing XBEL boomark listings.   It uses Python 2.2. generators for straightforward and efficient iteration over the XBEL DOM trees in document order.  It requires Python 2.2 and 4Suite 0.12.0a2 or more recent versions.
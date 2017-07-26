## Arbitrary order attribute writing with ElementTree  
Originally published: 2008-07-31 21:34:00  
Last updated: 2008-08-01 19:24:34  
Author: Orri Ganel  
  
Modified version of ElementTree with two additional parameters to the write() method: "sortflag" and "sortcmp".  "sortflag" defaults to "default", which results in unmodified behavior.  "sortcmp" defaults to None, which results in unmodified behavior.  See discussion for usage and justification.  Changes made begin on line 655.

EDIT: in most cases, unless sortflag happened to be intended for the root, it would be ignored; added sortflag and sortcmp to self._write() call on line 724.  Expect another revision in the near future to allow for specifying different orders for different xml tags.

EDIT, the second: Added tag-specific ordering.